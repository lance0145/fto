# -*- coding: utf-8 -*-

from flectra import models, fields, api
from flectra.tools.translate import _
from flectra.exceptions import UserError
from passlib.context import CryptContext

from ...fto_repository.tools import utilities

from flectra.addons import hr_recruitment
from flectra.addons import website_hr_recruitment

import logging
import time

_logger = logging.getLogger(__name__)

FTO_custom_logic = utilities.FTO_Custom_Logic()


class ApplicantDetails(models.Model):
    """
    In this method we will be creating custom tracking columns and adding them to an exisitng model.
    Using inheritance, we grab the hr.applicant model and extend it to include FTO specific model fields.
    We are adding these fields into the already created (hr.applicant), which will allow these fields
    to be available in the inherited model/class.
    """

    _inherit = ['hr.applicant']

    x_linkedin_url = fields.Text(
        string='LinkedIn URL', help='The LinkedIn profile/url of the applicant')
    x_years_of_experience = fields.Integer('Years of Experience', default=0)
    x_salary_previous = fields.Float(string='Previous Salary')
    x_test_type_results = fields.Char(string='Typing Test Results')
    x_test_speed_results = fields.Char(string='Speed Test Results')

    x_contact_address = fields.Char(string='Complete Address')
    x_ip_address = fields.Char(string='IP Address')
    x_longitude_latitude = fields.Char(
        string='Geographic Coordinates')

    x_res_partner_country_id = fields.Many2one(
        'res.country', ondelete='set null', string="Country", default=176)

    x_partner_name_first = fields.Char(required=True, string="First Name")
    x_partner_name_middle = fields.Char(required=True, string="Middle Name")
    x_partner_name_last = fields.Char(required=True, string="Last Name")

    x_res_partner_internet = fields.One2many('res.partner.internet', 'x_partner_id',
                                             compute="display_list_internet_details")
    x_res_partner_education = fields.One2many('res.partner.education', 'x_partner_id',
                                              compute="display_list_education_details")
    x_res_partner_identification = fields.One2many('res.partner.identification', 'x_partner_id',
                                                   compute="display_list_identification_details")

    def display_list_internet_details(self):
        for record in self:
            res_partner_id = record.partner_id and record.partner_id.id or False
            if res_partner_id:
                rec_ids = self.env['res.partner.internet'].search([('x_partner_id', '=', res_partner_id)])
                record.x_res_partner_internet = rec_ids.ids

    def display_list_education_details(self):
        for record in self:
            res_partner_id = record.partner_id and record.partner_id.id or False
            if res_partner_id:
                rec_ids = self.env['res.partner.education'].search([('x_partner_id', '=', res_partner_id)])
                record.x_res_partner_education = rec_ids.ids

    def display_list_identification_details(self):
        for record in self:
            res_partner_id = record.partner_id and record.partner_id.id or False
            if res_partner_id:
                rec_ids = self.env['res.partner.identification'].search([('x_partner_id', '=', res_partner_id)])
                record.x_res_partner_identification = rec_ids.ids        

    # if these fields are changed, call method
    @api.onchange('x_partner_name_first', 'x_partner_name_middle', 'x_partner_name_last')
    def _onchange_partner_name(self):
        self.partner_name = FTO_custom_logic.update_name_fields(
            self.x_partner_name_first, self.x_partner_name_middle, self.x_partner_name_last)

    # jobs apply update name
    @api.multi
    def website_form_input_filter(self, request, values):
        values['partner_name'] = FTO_custom_logic.update_name_fields(
            values['x_partner_name_first'], values['x_partner_name_middle'], values['x_partner_name_last'])
        if 'partner_name' in values:
            values.setdefault('name', '%s\'s Application' % values['partner_name'])
        return values

    website_hr_recruitment.models.hr_recruitment.Applicant.website_form_input_filter = website_form_input_filter

    # applicant fluency capture form
    @api.multi
    def action_openFluency(self):
        self.ensure_one()
        partners = self.partner_id | self.user_id.partner_id | self.department_id.manager_id.user_id.partner_id

        res_partner_rec = self.env['res.partner'].search([('id', '=', self.partner_id.id)])

        res = self.env['ir.actions.act_window'].for_xml_id(
            'fto_applicant', 'fto_fluency_capture_form_action_list_modal')
        res['context'] = {
            'default_partner_ids': partners.ids,
            'default_user_id': self.env.uid,
            'default_name': self.partner_name,
            'default_x_lnd_english_fluency': res_partner_rec.x_lnd_english_fluency,
            'default_id': res_partner_rec.id,
            'default_res_id': res_partner_rec.id,

        }
        res['res_id'] = res_partner_rec.id

        return res

    # applicant fluency capture form
    @api.multi
    def action_openOtherDetails(self):
        self.ensure_one()
        partners = self.partner_id | self.user_id.partner_id | self.department_id.manager_id.user_id.partner_id

        res_partner_rec = self.env['res.partner'].search(
            [('id', '=', self.partner_id.id)])

        res = self.env['ir.actions.act_window'].for_xml_id(
            'fto_applicant', 'fto_fluency_other_details_action_list_modal')
        res['context'] = {
            'default_partner_ids': partners.ids,
            'default_user_id': self.env.uid,
            'default_name': self.partner_name,
            'default_x_details_internet': res_partner_rec.x_details_internet,
            'default_x_details_education': res_partner_rec.x_details_education,
            'default_x_details_identification': res_partner_rec.x_details_identification,
            'default_id': res_partner_rec.id,
            'default_res_id': res_partner_rec.id,
        }
        res['res_id'] = res_partner_rec.id
        res['tag'] = 'reload'
        res['view_type'] = 'form'
        res['res_model'] = 'res.partner'
        return res




    # override write method for applicant
    @api.multi
    def write(self, vals):
        # add a record for the applicant's details
        record_id = self.env['res.partner'].search(
            [('id', '=', self.partner_id.id)]).id
        results = self.env['res.partner'].browse(record_id)

        if not results:
            partner = self.env['res.partner'].create({
                'is_company': False,
                'name': self.partner_name,
                'email': self.email_from,
                'phone': self.partner_phone,
                'mobile': self.partner_phone,
                'contact_address': self.x_contact_address,
                # flags
                'x_applicant': True,
                'res_partner_app_id': self.id
            })

            vals['partner_id'] = partner.id

        # execute the default method
        res = super(ApplicantDetails, self).write(vals)
        return res

    # override create method for applicant
    @api.model
    def create(self, vals):
        # add a record for the applicant's details
        partner_id = 0
        if "partner_id" in vals:
            partner_id = vals['partner_id']
        record_id = self.env['res.partner'].search(
            [('id', '=', partner_id)]).id
        results = self.env['res.partner'].browse(record_id)

        if not results:
            partner = self.env['res.partner'].create({
                'is_company': False,
                'name': vals['partner_name'],
                'email': vals['email_from'],
                'phone': vals['partner_phone'],
                'mobile': vals['partner_phone'],
                'contact_address': self.x_contact_address,
                # flags
                'x_applicant': True,
            })

            vals['partner_id'] = partner.id

        # execute the default method
        res = super(ApplicantDetails, self).create(vals)
        return res

    # override create emplyoee method from applicant
    @api.multi
    def create_employee_from_applicant(self):
        self.ensure_one()
        
        # execute the default method
        res = super(ApplicantDetails, self).create_employee_from_applicant()

        partner_id = 0
        if "partner_id" in self:
            partner_id = self.partner_id.id
        record_id = self.env['res.users'].search(
            [('partner_id', '=', partner_id)]).id
        results = self.env['res.users'].browse(record_id)

        if not results:

            password_str = 'fto_'+self.x_partner_name_last.lower().replace(" ", "_")

            # create user data
            employee_group = self.env.ref('base.group_user').id
            survey_group = self.env.ref('survey.group_survey_user').id

            user_rec = self.env['res.users'].create({
                'active': True,
                'login': self.email_from,
                'password': password_str,
                'partner_id': self.partner_id.id,  # reference as FK in res_partner
                'signature': 'Employee<span>',
                'x_user_name_first': self.x_partner_name_first,
                'x_user_name_middle': self.x_partner_name_middle,
                'x_user_name_last': self.x_partner_name_last,
                'groups_id': [(6, 0, [employee_group, survey_group])], # assign default group Employee.
            })

            resource_rec = self.env['resource.resource'].search(
                [('name', '=', self.partner_name)])
            resource_rec.write({
                'user_id': user_rec.id
            })



            # update employee data
            emp = self.env['hr.employee'].search(
                [('id', '=', self.emp_id.id)])
            emp.write({
                'x_employee_name_first': self.x_partner_name_first,
                'x_employee_name_middle': self.x_partner_name_middle,
                'x_employee_name_last': self.x_partner_name_last,
                'partner_id': self.partner_id.id
            })

            # update applicant field in res,partner
            record = self.env['res.partner'].search(
                [('id', '=', self.partner_id.id)])
            record.write({'x_applicant': False, 'employee': True})

            # return default values
            return res


    #disqualify button logic
    @api.multi
    def disqualify_applicant(self):
        self.write({'active': False})
        self.ensure_one()    
        template = self.env.ref('fto_applicant.disqualify_email_template', False,)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False,)
        ctx = dict(
            default_model='hr.applicant',
            default_res_id=self.id,
            default_use_template= bool(template),
            default_template_id= template and template.id or False,
            default_composition_mode= 'comment',
        )
        return {
            'name': _('Compose Disqualify Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        } 

