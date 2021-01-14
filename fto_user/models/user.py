# -*- coding: utf-8 -*-

from flectra import models, fields, api
from ...fto_repository.tools import utilities

FTO_custom_logic = utilities.FTO_Custom_Logic()


class User(models.Model):
    _inherit = ['res.users']

    x_user_name_first = fields.Char(string="Employee/User's First Name")
    x_user_name_middle = fields.Char(string="Employee/User's Middle Name")
    x_user_name_last = fields.Char(string="Employee/User's Last Name")

    @api.onchange('x_user_name_first', 'x_user_name_middle', 'x_user_name_last')  # if these fields are changed, call method
    def _onchange_user_name(self):
        self.name = FTO_custom_logic.update_name_fields(
            self.x_user_name_first, self.x_user_name_middle, self.x_user_name_last)

    @api.model
    def create(self, vals):
        res = super(User, self).create(vals)
        employee_group = self.env.ref('base.group_user').id
        survey_group = self.env.ref('survey.group_survey_user').id
        res.write({
            'groups_id': [(6, 0, [employee_group, survey_group])], # assign default group Employee.
        })
        return res