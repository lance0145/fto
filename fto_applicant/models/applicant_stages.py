# -*- coding: utf-8 -*-

from flectra import models, fields, api
from flectra.exceptions import UserError, ValidationError
import logging
import time
_logger = logging.getLogger(__name__)

class ApplicantDetails(models.Model):

	_inherit = ['hr.applicant']

	# check if applicant has a record on english fluency if not pop-up fluency 
	@api.multi
	def write(self, values):
		# execute the default method
		res = super(ApplicantDetails, self).write(values)

		record_id = self.env['res.partner'].search(
			[('id', '=', self.partner_id.id)]).id
		results = self.env['res.partner'].browse(record_id)

		if results:
			fluency = self.partner_id.x_lnd_english_fluency		
			stages = self.env['hr.recruitment.stage']
			if 'stage_id' in values:
				trigger_stage = stages.search([('id', '=', values['stage_id'])]).name
				if trigger_stage == 'Fluency Completed' or trigger_stage == 'Final Interview' or trigger_stage == 'Re-Hire' or trigger_stage == 'Contract Proposal':
					if fluency == 0.0: 
						# pop up fluency form if condition meet
						raise ValidationError('Applicant has no scored on English Fluency, Please insert score.')

		return res