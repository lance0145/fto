# -*- coding: utf-8 -*-

import re
import uuid

import base64
import json
import pytz

from flectra import http, _
from flectra.http import request
from flectra.tools import pycompat
from werkzeug import urls

from datetime import datetime
from psycopg2 import IntegrityError

from flectra import http
from flectra.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from flectra.tools.translate import _
from flectra.exceptions import ValidationError
from flectra.addons.base.ir.ir_qweb.fields import nl2br

import logging
import time
import requests, json#, socket

_logger = logging.getLogger(__name__)


class FTOApplicant(http.Controller):

	@http.route('/jobs/apply/<model("hr.job"):job>', type='http', auth="public", website=True)
	def jobs_apply(self, job, **kwargs):
		#internet_provider_rec = request.env['res.identification'].sudo().search([])
		#internet_provider_rec = dict(request.env['res.partner.internet.provider']._fields['name'].selection)
		internet_provider_rec = request.env['res.partner.internet.provider'].sudo().search([])
		#speed_rec = request.env['res.partner.internet'].sudo().search([])

		speed_rec = dict(request.env['res.partner.internet']._fields['x_speed'].selection)
		type_rec = request.env['res.partner.internet.type'].sudo().search([])
		plan_rec = request.env['res.partner.internet.plan'].sudo().search([])

		identification_rec = request.env['res.identification'].sudo().search([])
		
		#education dropdown
		education_level_rec = request.env['res.partner.education.level'].sudo().search([])
		education_course_rec = request.env['res.partner.education.course'].sudo().search([])
		x_year_rec = dict(request.env['res.partner.education']._fields['x_year'].selection)

		error = {}
		default = {}

		if 'website_hr_recruitment_error' in request.session:
			error = request.session.pop('website_hr_recruitment_error')
			default = request.session.pop('website_hr_recruitment_default')

		# check if job location has a value if not check user ip of the user to get his/her country code to filter relevant id's for his/her country.
		if job.x_branch_id.sudo().country_id:
			check_country_rec = job.x_branch_id.sudo().country_id.code
		else:
			ip = request.httprequest.environ['REMOTE_ADDR']
			response = requests.get("https://ipinfo.io/{}/country?token=cb5132994d591e".format(ip))
			check_country_rec = response.text[:2]

		return request.render("website_hr_recruitment.apply", {
			'job': job,
			'error': error,
			'default': default,
			'identification_rec': identification_rec,
			'internet_provider_rec': internet_provider_rec,
			'speed_rec': speed_rec,
			'plan_rec': plan_rec,
			'type_rec': type_rec,
			'education_level_rec': education_level_rec,
			'education_course_rec': education_course_rec,
			'x_year_rec': x_year_rec,
			'check_country_rec': check_country_rec,
		})

	@http.route('/job-thank-you', type='http', auth="public", website=True)
	def jobs_thankyou(self, **kwargs):
		def create_token(survey_id, partner_id, email):
			SurveyUserInput = request.env['survey.user_input']

			# check if applicant has already a record in survey
			survey_user_input = SurveyUserInput.sudo().search([('survey_id', '=', survey_id),
				('partner_id', '=', partner_id),
				('email', '=', email)], order='id DESC', limit=1)
			if survey_user_input:
				return survey_user_input.token
			else:
				#if no record create a new one
				token = pycompat.text_type(uuid.uuid4())

				survey_user_input = SurveyUserInput.create({
				'survey_id': survey_id,
				'deadline': None,
				'type': 'link',
				'state': 'new',
				'token': token,
				'partner_id': partner_id,
				'email': email})
				return survey_user_input.token

		res_applicant_id = 0
		res_partner_id = 0
		assessments = []
		if request.session['form_builder_model_model'] == 'hr.applicant':
			res_applicant_id = request.session['form_builder_id']
			res_applicant_rec = request.env['hr.applicant'].sudo().search([('id', '=', res_applicant_id)])
			job_survey_id = request.env['hr.job'].sudo().search([('id', '=', res_applicant_rec.job_id.id)])

			res_partner_id = res_applicant_rec.partner_id.id

			#for assessments
			if job_survey_id.x_job_assessment_ids:
				for job_assessment in job_survey_id.x_job_assessment_ids:
					assessment_url_id = request.env['survey.survey'].sudo().search([('id', '=', job_assessment.id)])
					assessment_url = assessment_url_id.public_url
					assessment_url = urls.url_parse(assessment_url).path[1:]

					assessment_token = create_token(job_assessment.id, res_partner_id, res_applicant_rec.email_from)

					if assessment_token:
						assessment_url = assessment_url + '/' + assessment_token

					assessments.append({
						'title':job_assessment.title,
						'url':assessment_url,
						'token':assessment_token,
					})

		error = {}
		default = {} 
		if 'website_hr_recruitment_error' in request.session:
			error = request.session.pop('website_hr_recruitment_error')
			default = request.session.pop('website_hr_recruitment_default')
		return request.render("website_hr_recruitment.thankyou", {
			'res_applicant_id': res_applicant_id,
			'res_partner_id': res_partner_id,
			'assessments': assessments,
			'error': error,
			'default': default,
		})
	

	# Check and insert values from the form on the model <model>
	@http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
	def website_form(self, model_name, **kwargs):
		if (model_name == 'hr.applicant'):
			model_record = request.env['ir.model'].sudo().search([('model', '=', model_name), ('website_form_access', '=', True)])
			if not model_record:
				return json.dumps(False)

			try:
				data = self.extract_data(model_record, request.params)
			# If we encounter an issue while extracting data
			except ValidationError as e:
				# I couldn't find a cleaner way to pass data to an exception
				return json.dumps({'error_fields' : e.args[0]})

			try:
				id_record = self.insert_record(request, model_record, data['record'], data['custom'], data.get('meta'))
				if id_record:
					self.insert_attachment(model_record, id_record, data['attachments'])

			# Some fields have additional SQL constraints that we can't check generically
			# Ex: crm.lead.probability which is a float between 0 and 1
			# TODO: How to get the name of the erroneous field ?
			except IntegrityError:
				return json.dumps(False)

			request.session['form_builder_model_model'] = model_record.model
			request.session['form_builder_model'] = model_record.name
			request.session['form_builder_id'] = id_record

			res_applicant_rec = request.env['hr.applicant'].sudo().search([('id', '=', id_record)])

			res_partner_id = res_applicant_rec.partner_id.id

			request.session['x_partner_id'] = res_partner_id
			return json.dumps({'id': id_record, 'partner_id': res_partner_id})

		else:

			if (model_name == 'hr.applicant.assessment.test'):
				values = {
					'id': '',
					'x_test_type_results': '',
					'x_test_speed_results': '',
				}
				try: 
					for field_name, field_value in request.params.items():	
						if field_name == 'x_applicant_id':
							values['id'] = field_value
						elif field_name == 'test_type_results':
							values['x_test_type_results'] = field_value
						elif field_name == 'test_speed_results':
							values['x_test_speed_results'] = field_value

					if values['id']:
						applicant_rec = request.env['hr.applicant'].sudo().search([('id', '=', values['id'])])
						for rec in applicant_rec:
							record = rec.sudo().write({'x_test_type_results': values['x_test_type_results'],'x_test_speed_results': values['x_test_speed_results']})
						return json.dumps({'id': values['id']})
				except IntegrityError:
					return json.dumps(False)

			model_record = request.env['ir.model'].sudo().search([('model', '=', model_name)])
			
			if not model_record:
				return json.dumps(False)

			if (model_name == 'res.partner.identification'):
				x_partner_id = False
				try:
					params = {
						'record': {},        # Values to create record
						'attachments': [],  # Attached files
						'custom': '',        # Custom fields values
						'meta': '',         # Add metadata if enabled
					}
					id_records = []
					for field_name, field_value in request.params.items():
						if field_name == 'x_partner_id':
							x_partner_id = field_value

					for field_name, field_value in request.params.items():
						if field_name != 'x_partner_id':
							params['record']['x_partner_id'] = x_partner_id
							params['record']['x_identification_id'] = field_name
							params['record']['x_value'] = field_value
							params['custom'] = None

							id_record = self.insert_record(request, model_record, params['record'], params['custom'], None)
							id_records.append(id_record)

					return json.dumps({'ids': id_records})			

				# Some fields have additional SQL constraints that we can't check generically
				# Ex: crm.lead.probability which is a float between 0 and 1
				# TODO: How to get the name of the erroneous field ?
				except IntegrityError:
					return json.dumps(False)

			else:

				try:
					data = self.extract_data(model_record, request.params)

				# If we encounter an issue while extracting data
				except ValidationError as e:
					# I couldn't find a cleaner way to pass data to an exception
					return json.dumps({'error_fields' : e.args[0]})

				try:

					id_record = self.insert_record(request, model_record, data['record'], data['custom'], data.get('meta'))
					if id_record:
						self.insert_attachment(model_record, id_record, data['attachments'])

				# Some fields have additional SQL constraints that we can't check generically
				# Ex: crm.lead.probability which is a float between 0 and 1
				# TODO: How to get the name of the erroneous field ?
				except IntegrityError:
					return json.dumps(False)

				return json.dumps({'id': id_record})
			

	# Constants string to make custom info and metadata readable on a text field

	_custom_label = "%s\n___________\n\n" % _("Custom infos")  # Title for custom fields
	_meta_label = "%s\n________\n\n" % _("Metadata")  # Title for meta data

	# Dict of dynamically called filters following type of field to be fault tolerent

	def identity(self, field_label, field_input):
		return field_input

	def integer(self, field_label, field_input):
		return int(field_input)

	def floating(self, field_label, field_input):
		return float(field_input)

	def boolean(self, field_label, field_input):
		return bool(field_input)

	def date(self, field_label, field_input):
		lang = request.env['ir.qweb.field'].user_lang()
		return datetime.strptime(field_input, lang.date_format).strftime(DEFAULT_SERVER_DATE_FORMAT)

	def datetime(self, field_label, field_input):
		lang = request.env['ir.qweb.field'].user_lang()
		strftime_format = (u"%s %s" % (lang.date_format, lang.time_format))
		user_tz = pytz.timezone(request.context.get('tz') or request.env.user.tz or 'UTC')
		dt = user_tz.localize(datetime.strptime(field_input, strftime_format)).astimezone(pytz.utc)
		return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

	def binary(self, field_label, field_input):
		return base64.b64encode(field_input.read())

	def one2many(self, field_label, field_input):
		return [int(i) for i in field_input.split(',')]

	def many2many(self, field_label, field_input, *args):
		return [(args[0] if args else (6,0)) + (self.one2many(field_label, field_input),)]

	_input_filters = {
		'char': identity,
		'text': identity,
		'html': identity,
		'date': date,
		'datetime': datetime,
		'many2one': integer,
		'one2many': one2many,
		'many2many':many2many,
		'selection': identity,
		'boolean': boolean,
		'integer': integer,
		'float': floating,
		'binary': binary,
	}


	# Extract all data sent by the form and sort its on several properties
	def extract_data(self, model, values):

		data = {
			'record': {},        # Values to create record
			'attachments': [],  # Attached files
			'custom': '',        # Custom fields values
			'meta': '',         # Add metadata if enabled
		}

		authorized_fields = model.sudo()._get_form_writable_fields()
		error_fields = []


		for field_name, field_value in values.items():
			# If the value of the field if a file
			if hasattr(field_value, 'filename'):
				# Undo file upload field name indexing
				field_name = field_name.split('[', 1)[0]

				# If it's an actual binary field, convert the input file
				# If it's not, we'll use attachments instead
				if field_name in authorized_fields and authorized_fields[field_name]['type'] == 'binary':
					data['record'][field_name] = base64.b64encode(field_value.read())
					field_value.stream.seek(0) # do not consume value forever
				else:
					field_value.field_name = field_name
					data['attachments'].append(field_value)

			# If it's a known field
			elif field_name in authorized_fields:
				try:
					input_filter = self._input_filters[authorized_fields[field_name]['type']]
					data['record'][field_name] = input_filter(self, field_name, field_value)
				except ValueError:
					error_fields.append(field_name)

			# If it's a custom field
			elif field_name != 'context':
				data['custom'] += u"%s : %s\n" % (field_name, field_value)

		# Add metadata if enabled
		environ = request.httprequest.headers.environ
		if(request.website.website_form_enable_metadata):
			data['meta'] += "%s : %s\n%s : %s\n%s : %s\n%s : %s\n" % (
				"IP"                , environ.get("REMOTE_ADDR"),
				"USER_AGENT"        , environ.get("HTTP_USER_AGENT"),
				"ACCEPT_LANGUAGE"   , environ.get("HTTP_ACCEPT_LANGUAGE"),
				"REFERER"           , environ.get("HTTP_REFERER")
			)

		# This function can be defined on any model to provide
		# a model-specific filtering of the record values
		# Example:
		# def website_form_input_filter(self, values):
		#     values['name'] = '%s\'s Application' % values['partner_name']
		#     return values
		dest_model = request.env[model.sudo().model]
		if hasattr(dest_model, "website_form_input_filter"):
			data['record'] = dest_model.website_form_input_filter(request, data['record'])

		missing_required_fields = [label for label, field in authorized_fields.items() if field['required'] and not label in data['record']]
		if any(error_fields):
			raise ValidationError(error_fields + missing_required_fields)

		return data

	def insert_record(self, request, model, values, custom, meta=None):
		model_name = model.sudo().model
		record = request.env[model_name].sudo().with_context(mail_create_nosubscribe=True).create(values)

		if custom or meta:
			default_field = model.website_form_default_field_id
			default_field_data = values.get(default_field.name, '')
			custom_content = (default_field_data + "\n\n" if default_field_data else '') \
						   + (self._custom_label + custom + "\n\n" if custom else '') \
						   + (self._meta_label + meta if meta else '')

			# If there is a default field configured for this model, use it.
			# If there isn't, put the custom data in a message instead
			if default_field.name:
				if default_field.ttype == 'html' or model_name == 'mail.mail':
					custom_content = nl2br(custom_content)
				record.update({default_field.name: custom_content})
			else:
				values = {
					'body': nl2br(custom_content),
					'model': model_name,
					'message_type': 'comment',
					'no_auto_thread': False,
					'res_id': record.id,
				}
				mail_id = request.env['mail.message'].sudo().create(values)

		return record.id

	# Link all files attached on the form
	def insert_attachment(self, model, id_record, files):
		orphan_attachment_ids = []
		model_name = model.sudo().model
		record = model.env[model_name].browse(id_record)
		authorized_fields = model.sudo()._get_form_writable_fields()
		for file in files:
			custom_field = file.field_name not in authorized_fields
			attachment_value = {
				'name': file.field_name if custom_field else file.filename,
				'datas': base64.encodestring(file.read()),
				'datas_fname': file.filename,
				'res_model': model_name,
				'res_id': record.id,
			}
			attachment_id = request.env['ir.attachment'].sudo().create(attachment_value)
			if attachment_id and not custom_field:
				record.sudo()[file.field_name] = [(4, attachment_id.id)]
			else:
				orphan_attachment_ids.append(attachment_id.id)

		if model_name != 'mail.mail':
			# If some attachments didn't match a field on the model,
			# we create a mail.message to link them to the record
			if orphan_attachment_ids:
				values = {
					'body': _('<p>Attached files : </p>'),
					'model': model_name,
					'message_type': 'comment',
					'no_auto_thread': False,
					'res_id': id_record,
					'attachment_ids': [(6, 0, orphan_attachment_ids)],
				}
				mail_id = request.env['mail.message'].sudo().create(values)
		else:
			# If the model is mail.mail then we have no other choice but to
			# attach the custom binary field files on the attachment_ids field.
			for attachment_id_id in orphan_attachment_ids:
				record.attachment_ids = [(4, attachment_id_id)]
