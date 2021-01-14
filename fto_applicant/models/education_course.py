# -*- coding: utf-8 -*-

from flectra import models, fields, api

class EducationCourse(models.Model):
	"""
	This method is being defined to ensure proper tracking of educational information for Applicants.
	The Education method connects with this one to grab the education course field and 
	this is where we define the model to hold predefined data for Education Course Names; Allowing
	Applicants to choose a field of study(course) and have it stored to their record.
	"""

	_name = 'res.partner.education.course'

	x_name = fields.Char(string="Course Name", required=True, readonly=True)
