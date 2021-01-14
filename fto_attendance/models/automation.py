# -*- coding: utf-8 -*-

import logging

from flectra import api, models
from flectra.exceptions import AccessDenied
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class GenerateDailyRecords(models.AbstractModel):
    """ Expose the vacuum method to the cron jobs mechanism. """
    _name = 'fto.generatedailyrecords'

    @api.model
    def _generate(self):
        self.env.cr.execute("SELECT id, name, company_id FROM hr_employee"
                   " WHERE active = True"
                   "   AND x_calendar_id IS NOT NULL")
        for uid, name, company_id in self.env.cr.fetchall():
            self.sudo()._get_resource_calendar_record(name,company_id,uid)

    @api.model
    def _get_resource_calendar_record(self, name, company_id, employee_id):
        if employee_id:
            result = self.env['resource.calendar'].search([('name', '=', name)])

            if result:
                self.sudo()._create_resource_calendar_fto_attendance_record(result.id)

    @api.model
    def _create_resource_calendar_fto_attendance_record(self, calendar_id):

        # THE DAILY RECORDS SHOULD BE GENERATED A MONTH IN ADVANCE.
        attendance_date = date.today() + relativedelta(months=+1)

        #THE DAILY RECORDS WILL NOT HAVE ANY VALUES INPUTTED FOR THE SHIFT_ID and ATTENDANCE_IDS
        res = self.env['resource.calendar.fto.attendance'].create({
                'calendar_id': calendar_id,
                'attendance_date': attendance_date,
            })

    @api.model
    def power_on(self, *args, **kwargs):
        if not self.env.user._is_admin():
            raise AccessDenied()

        self._generate()
        return True