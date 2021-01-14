# Copyright (C) 2020 Fair Trade Outsourcing
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from flectra import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class SurveyMaxScoreAndPercentage(models.Model):

	"""
	This method will allow us to define custom model references for survey.user_input and add any necessary columns.
	We add an 2  column to the survey.user_input model,
	"""

	_inherit = 'survey.user_input'
		
	x_quizz_max_score = fields.Float(string="Maximum score for the quiz", digits=(4,3), store=True, readonly=True, compute="_compute_max_score_and_percentage")
	x_quizz_score_percentage =  fields.Float(string="Score Percentage", digits=(4,3) , store=True, readonly=True, compute="_compute_max_score_and_percentage")  

	@api.depends('survey_id','quizz_score')
	def _compute_max_score_and_percentage(self):
		for record in self:
			pages = self.env['survey.page']
			page_ids = pages.search([('survey_id', '=', record.survey_id.id)])
			max_score = 0
			if page_ids:
				for page in page_ids:
					questions = self.env['survey.question']
					question_ids = questions.search([('page_id', '=', page.id)])
					if question_ids:
						for question in question_ids:
							survey_labels = self.env['survey.label']
							survey_labels_ids = survey_labels.search([('question_id', '=', question.id)])

							if survey_labels_ids:
								highest_val = 0
								for survey_label in survey_labels_ids:
									if question.type == 'simple_choice':
										highest_val = survey_label.quizz_mark > highest_val and survey_label.quizz_mark or highest_val 
									elif question.type == 'multiple_choice':
										highest_val += survey_label.quizz_mark
									
								max_score += highest_val

			record.x_quizz_max_score = max_score	
			if record.quizz_score > 0:
				record.x_quizz_score_percentage = (record.quizz_score / max_score) * 100
			else:
				record.x_quizz_score_percentage = 0				

	# override write method for inserting record in survey_user_input
	@api.multi
	def write(self, vals):

		# execute the default method
		res = super(SurveyMaxScoreAndPercentage, self).write(vals)

		for record in self:
			partners = self.env['res.partner'].search([('id', '=', record.partner_id.id)])
			for partner in partners:
				if record.survey_id.x_type_id.name == "English Proficiency":
					partner.write({'x_lnd_english_proficiency': record.x_quizz_score_percentage})
				if record.survey_id.x_type_id.name == "Computer Operation":
					partner.write({'x_lnd_computer_operation': record.x_quizz_score_percentage})
				if record.survey_id.x_type_id.name == "Customer Service":
					partner.write({'x_lnd_customer_service ': record.x_quizz_score_percentage})

		return res


class SurveyType(models.Model):
	_name = "survey.type"
	name = fields.Char(string='Type',required=True)

class SurveyEnumeration(models.Model):
	_inherit = ["survey.survey"]
	
	x_type_id = fields.Many2one('survey.type', string='Survey Type', required=True)# default=1)
	x_enumeration = fields.Integer(string='Enumeration')

	@api.onchange('x_type_id')
	def get_max_enumeration(self):
		# get the last highest enumeration of the same type
		last_record = self.env['survey.survey'].search([('x_type_id','=',self.x_type_id.id)], order='id desc', limit = 1)
		max1 = 0
		max1 = last_record.x_enumeration + 1
		self.x_enumeration = max1