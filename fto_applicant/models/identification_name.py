# -*- coding: utf-8 -*-

from flectra import models, fields, api


class IdentificationName(models.Model):
	""" 
	This method is being defined to ensure proper tracking of identification information for Applicants. 
	This will be leveraging the existing res.partner model that also ties back to eventual Employees.
	In this method, we create the following model fields: name, description and country_id which can be used
	in combination with res.partner.identification model so we can correctly capture identifcation for applicants, Employess/Users
	"""

	_name = "res.identification"
	x_name = fields.Char(string="Identification Name", required=True)
	x_description = fields.Text(string="Description")

	x_country_id = fields.Many2one(
		'res.country', ondelete='set null', string="Country")
