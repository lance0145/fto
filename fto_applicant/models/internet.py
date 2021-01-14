# -*- coding: utf-8 -*-
# Developer : Allan Abendanio
# Date : 25-Sep-2020
# Add New Fields for Internet Provider, Internet Plan, Internet Type

from flectra import models, fields, api

class provider(models.Model):
	_name = 'res.partner.internet.provider'
	x_name = fields.Char(string="Provider", required=True)
	x_description = fields.Text(string='Description')

class plan(models.Model):
	_name = 'res.partner.internet.plan'
	x_name = fields.Char(string="Plan", required=True)
	x_description = fields.Text(string='Description')

class type(models.Model):
	_name = 'res.partner.internet.type'
	x_name = fields.Char(string="Type", required=True)
	x_description = fields.Text(string='Description')

class internet(models.Model):
	_name = 'res.partner.internet'
	x_speed = fields.Selection([
			('10', '1 - 10 Mbps'),
			('25', '11 - 25 Mbps'),
			('50', '26 - 50 Mbps'),
			('100', '51 - 100 Mbps'),
			('250', '101 - 250 Mbps'),
			('500', '251 - 500 Mbps'),
			('1000', '501 - 1000 Mbps'),
			('0', 'Unknown')
			], string='Speed')

	x_partner_id = fields.Many2one('res.partner', string='Contact Name')
	x_provider_id = fields.Many2one('res.partner.internet.provider', string='Provider Id')
	x_plan_id = fields.Many2one('res.partner.internet.plan', string='Plan Id')
	x_type_id = fields.Many2one('res.partner.internet.type', string='Type Id')
	x_rate = fields.Integer(string='Monthly Rate')
	x_account_holder = fields.Char(string='Account Holder')
	x_details = fields.Text(string='Detail')

