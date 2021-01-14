# Developer : Surendra Gupta
#Date : 12-Sep-2020
# Add New Fields for Course, Level, School - Applicant Id


import base64
import logging

from flectra import api, fields, models

class Institution(models.Model):
	"""
	This method is being defined to ensure proper tracking of educational information for Applicants.
	This will be leveraging the existing res.partner model that also ties back to eventual Employees.
	We grab the exsisting model(res.partner) and extend it to include FTO specific model fields(institution_name)
	With this, we can store the name of the Institution from which the user studied at
	"""

	_name = 'res.institution'
	x_name = fields.Char(string="Institution Name", required=True)
