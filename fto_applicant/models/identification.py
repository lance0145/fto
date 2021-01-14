# -*- coding: utf-8 -*-

from flectra import models, fields, api


class Identification(models.Model):
	"""
	This method is being defined to ensure proper tracking of identification information for Applicants. 
	This will be leveraging the existing res.partner model that also ties back to eventual Employees.
	We grab the exsisting model and extend it to include FTO specific model fields(parter_id, identification_id, value) 
	in addition to the already provided base fields in the res.partner model. 
	"""

	_name = "res.partner.identification"


	x_partner_id = fields.Many2one(
		'res.partner', ondelete='set null', string="Contact Name", required=True, index=True)

	x_identification_id = fields.Many2one(
		'res.identification', ondelete='set null', string="Identification Name", required=True)

	x_value = fields.Char(string="Identification Value", required=True)

