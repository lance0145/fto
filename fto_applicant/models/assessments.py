# -*- coding: utf-8 -*-

import re
import uuid
from flectra.tools import pycompat
from werkzeug import urls
from flectra import models, fields, api
from flectra.exceptions import UserError, ValidationError


class DisplayAssessments(models.Model):
	_inherit = "hr.applicant"

	x_surveys_assessments = fields.One2many('survey.user_input','partner_id',compute="display_list_assessments")

	def display_list_assessments(self):
		assessments = []
		for record in self:
			res_partner_id = record.partner_id and record.partner_id.id or False
			if res_partner_id:
				survey_input_ids = self.env['survey.user_input'].search([('partner_id', '=', res_partner_id)])
				record.x_surveys_assessments = survey_input_ids.ids

class SendAssessments(models.Model):
	_inherit = "hr.applicant"

	# override write method for applicant
	@api.model
	def create(self, vals):

		# execute the default method
		res = super(SendAssessments, self).create(vals)

		assessments_list = self.get_survey_assessments()
		#email survey and assessments
		body_html = "<p>Hi, %s</p>" % self.x_partner_name_first  
		body_html += """<p>Please complete the assessment(s) referenced below at your earliest convenience.
						The final application is not completed until the assessment(s) have been completed.</p>"""

		if assessments_list:
			for record in assessments_list:
				if record['survey']:
					for survey_rec in record['survey']:
						body_html += "<p><strong>%s </strong>" % survey_rec['title']
						body_html += """ <a href="%s" target="_blank" style="background-color: #1abc9c; padding: 5px 10px; font-weight: bold; text-decoration: none; color: #fff; border-radius: 5px; font-size:14px;">Link</a>
										</p>""" % survey_rec['url']
				if record['assessments']:
					for assessment_rec in record['assessments']:
						body_html += "<p><strong>%s </strong>" % assessment_rec['title']
						body_html += """ <a href="%s" target="_blank" style="background-color: #1abc9c; padding: 5px 10px; font-weight: bold; text-decoration: none; color: #fff; border-radius: 5px; font-size:14px;">Link</a>
										</p>""" % assessment_rec['url']

		# post the message
		values = {
			'subject': "Assessment(s): %s" % self.job_id.name,
			'body_html': body_html,
		}

		values['email_to'] = self.email_from
		mail_id = self.env['mail.mail'].sudo().create(values)
		mail_id.sudo().send()

		return res

	@api.multi
	def get_survey_assessments(self):

		def create_token(survey_id, partner_id, email):
			SurveyUserInput = self.env['survey.user_input']

			# check if applicant has already a record in survey
			survey_user_input = SurveyUserInput.search([('survey_id', '=', survey_id),
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

		for record in self:
			res_partner_id = record.partner_id and record.partner_id.id or False
			survey = []
			assessments = []
			if res_partner_id:
				job_survey_id = self.env['hr.job'].sudo().search([('id', '=', record.job_id.id)])					

				#for assessments
				if job_survey_id.x_job_assessment_ids:
					for job_assessment in job_survey_id.x_job_assessment_ids:
						assessment_url_id = self.env['survey.survey'].sudo().search([('id', '=', job_assessment.id)])
						assessment_url = assessment_url_id.public_url
						assessment_url = urls.url_parse(assessment_url).path[1:]

						assessment_token = create_token(job_assessment.id, res_partner_id, record.email_from)

						if assessment_token:
							assessment_url = assessment_url + '/' + assessment_token

						assessments.append({
							'title':job_assessment.title,
							'url':assessment_url,
							'token':assessment_token,
						})
				
				records=[]
				items={}

				items['survey'] = survey
				items['assessments'] = assessments
				records.append(items)

				record.x_survey_assessments = records
				return records



class ResendAssessment(models.Model):

	_inherit = 'survey.survey'
	@api.multi
	def action_send_survey(self):
		""" Had to copy the whole method just to change the template id referencing """
		if not self.page_ids or not [page.question_ids for page in self.page_ids if page.question_ids]:
			raise UserError(_('You cannot send an invitation for a survey that has no questions.'))

		if self.stage_id.closed:
			raise UserError(_("You cannot send invitations for closed surveys."))
		
		template = self.env.ref('fto_applicant.email_template_resend_assessment', raise_if_not_found=False)

		local_context = dict(
			self.env.context,
			default_model='survey.survey',
			default_res_id=self.id,
			default_survey_id=self.id,
			default_use_template=bool(template),
			default_template_id=template and template.id or False,
			default_composition_mode='comment'
		)
		return {
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'survey.mail.compose.message',
			'target': 'new',
			'context': local_context,
		}