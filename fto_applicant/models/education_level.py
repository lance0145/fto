# -*- coding: utf-8 -*-

from flectra import models, fields, api


class EducationLevel(models.Model):

    """
    This method is being defined to ensure proper tracking of educational information for Applicants.
    The Education method connects with this one to grab the education level field and 
    this is where we define the model to hold predefined data for Education Level Names; Allowing
    Applicants to choose a Level and have it stored to their record.
    """

    _name = 'res.partner.education.level'

    x_name = fields.Char(string="Level Name", required=True, readonly=True)
