# -*- coding: utf-8 -*-

from flectra import models, fields, api

class ApplicantionCenter(models.Model):
	_inherit = "res.partner"

	user_id = fields.Many2one('res.users', default=lambda self: self.env.uid)
