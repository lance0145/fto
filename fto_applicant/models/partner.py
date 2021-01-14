# -*- coding: utf-8 -*-
from flectra import models, fields, api, _
from flectra.exceptions import UserError, ValidationError


class Partner(models.Model):
    """
    This method will allow us to define custom model inheritance references for res.partner and add any necessary columns.
    We add an applicant column to the res.partner model, and set it to be false by default.
    This means partners are not applicants unless specifically assigned.
    """

    _inherit = 'res.partner'

    x_applicant = fields.Boolean("Is Applicant", default=False)
    # res_partner_app_id = fields.Integer('Partner Res. FK', default='0', readonly=True)
    x_lnd_english_proficiency = fields.Float(digits=(4, 2), string="English Proficiency")
    x_lnd_computer_operation = fields.Float(digits=(4, 2), string="Computer Operation")
    x_lnd_customer_service = fields.Float(digits=(4, 2), string="Customer Service")
    x_lnd_english_fluency = fields.Float(digits=(4, 2), string="English Fluency")
    x_lnd_english_rating = fields.Float(digits=(4, 2), string="English Rating", compute="_compute_rating", store=True)

    x_details_internet = fields.One2many('res.partner.internet', 'x_partner_id', string='Internet', default=None)
    x_details_education = fields.One2many('res.partner.education', 'x_partner_id', string='Education', default=None)
    x_details_identification = fields.One2many('res.partner.identification', 'x_partner_id', string='Identification',
                                               default=None)

    @api.depends('x_lnd_english_proficiency', 'x_lnd_english_fluency')
    def _compute_rating(self):
        for r in self:
            if not r.x_lnd_english_fluency:
                r.x_lnd_english_rating = 0.0
            else:
                r.x_lnd_english_rating = (r.x_lnd_english_proficiency + r.x_lnd_english_fluency) / 2

    #constraint
    @api.constrains('x_lnd_english_proficiency','x_lnd_computer_operation','x_lnd_customer_service','x_lnd_english_fluency')
    @api.one
    def _check_number(self):
        number_fields = ['x_lnd_english_proficiency','x_lnd_computer_operation','x_lnd_customer_service','x_lnd_english_fluency']

        for rec in self:
            for keys in number_fields:
                number = rec[keys]
                if number > 100:
                    raise ValidationError(_('Number must not exceed to 100'))


    # override res.partner other details saving
    def action_saveOtherDetails(self):

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
