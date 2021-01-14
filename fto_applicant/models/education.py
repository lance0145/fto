# -*- coding: utf-8 -*-

from flectra import models, fields, api
from datetime import date, datetime


class Education(models.Model):
    """
    This method is being defined to ensure proper tracking of educational information for Applicants.
    This will be leveraging the existing res.partner model that also ties back to eventual Employees.
    We extend the exsisting model(res.partner) to include FTO specific model fields(partner_id, institution_id, year, level_id and course_id)
    This will be part of the Educational Capture for Contacts Data Model Breakdown (Applicants + Employees/Users).
    """

    _name = 'res.partner.education'

    x_partner_id = fields.Many2one(
        'res.partner', ondelete='set null', string="Contact Name", required=True, index=True)
    # x_institution_id = fields.Many2one(
    #     'res.institution', ondelete='set null', string="Institution Name", required=True)

    x_institution_name = fields.Char(string="Institution", required=True)

    #x_year = fields.Char(string="Year Graduate", size=4)
    x_year = fields.Selection([(num, str(num)) for num in range(1950, (datetime.now().year)+1 )], "Year Graduated")

    x_level_id = fields.Many2one('res.partner.education.level',
                                 ondelete='set null', string="Education Level", required=True)
    x_course_id = fields.Many2one(
        'res.partner.education.course', ondelete='set null', string="Course", required=True)

