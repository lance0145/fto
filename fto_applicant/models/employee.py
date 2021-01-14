# -*- coding: utf-8 -*-

from flectra import models, fields, api


class Employee(models.Model):

    _inherit = ['hr.employee']    

    # x_employee_name_first = fields.Char(string="Employee/User's First Name")
    # x_employee_name_middle = fields.Char(string="Employee/User's Middle Name")
    # x_employee_name_last = fields.Char(string="Employee/User's Last Name")