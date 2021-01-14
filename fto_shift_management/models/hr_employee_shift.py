# -*- coding: utf-8 -*-
###################################################################################
#    A part of OpenHrms Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Saritha Sahadevan (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from flectra import models, fields, api, _
from flectra import exceptions
from datetime import date, datetime, timedelta
from flectra.tools import DEFAULT_SERVER_DATETIME_FORMAT

import logging
from datetime import datetime
import time
_logger = logging.getLogger(__name__)


class HrEmployeeInherited(models.Model):
    _inherit = 'hr.employee'
    x_shift_schedule_ids = fields.One2many('hr.shift.schedule','x_employee_id', string="Shift", copy=True)
    #resource_calendar_ids = fields.Many2one('resource.calendar', 'Working Hours')


class HrEmployeeShift(models.Model):
    _inherit = 'resource.calendar'
    
    color = fields.Integer(string='Color Index')
    """def _get_default_attendance_ids(self):
        return [
            (0, 0, {'name': _('Monday Morning'), 'dayofweek': '0', 'hour_from': 8, 'hour_to': 12}),
            (0, 0, {'name': _('Tuesday Morning'), 'dayofweek': '1', 'hour_from': 8, 'hour_to': 12}),
            (0, 0, {'name': _('Wednesday Morning'), 'dayofweek': '2', 'hour_from': 8, 'hour_to': 12}),
            (0, 0, {'name': _('Thursday Morning'), 'dayofweek': '3', 'hour_from': 8, 'hour_to': 12}),
            (0, 0, {'name': _('Friday Morning'), 'dayofweek': '4', 'hour_from': 8, 'hour_to': 12}),
        ]

    hr_department = fields.Many2one('hr.department', string="Department", required=True)
    sequence = fields.Integer(string="Sequence", required=True, default=1)
    attendance_ids = fields.One2many(
        'resource.calendar.attendance', 'calendar_id', 'Workingssss Time',
        copy=True, default=_get_default_attendance_ids)

    @api.constrains('sequence')
    def validate_seq(self):
        record = self.env['resource.calendar'].search([('hr_department', '=', self.hr_department.id),
                                                       ('sequence', '=', self.sequence)
                                                       ])
        if len(record) > 1:
            raise ValidationError("One record with same sequence is already active."
                                  "You can't activate more than one record  at a time")"""



class HrSchedule(models.Model):
    _name = 'hr.shift.schedule'
    _order = 'x_hours_from desc'

    #start_date = fields.Date(string="Date From", required=True)
    #end_date = fields.Date(string="Date To", required=True)
    #hr_shift = fields.Many2one('resource.calendar', string="Shift", required=True)

    def _default_shift_type(self):
        return self.env['hr.shift.schedule.type'].search([('x_name', '=', 'Normal')], limit=1).id

    #rel_hr_schedule = fields.Many2one('hr.contract', ondelete='set null', string="Contract Name", required=True, index=True)
    x_hours_from = fields.Datetime(string="Work From", required=True)
    x_hours_to = fields.Datetime(string="Work To", required=True)
    x_shift_type = fields.Many2one('hr.shift.schedule.type', string="Shift Type", required=True, default=_default_shift_type)
    x_hours_billable = fields.Float(string="Billable Hours", required=True)
    x_department_id = fields.Many2one('hr.department', string="Department", ondelete='set null', required=True)
    x_employee_id = fields.Many2one('hr.employee', string="Employee", ondelete='set null', required=True)
    last_status = fields.Char(string='Status', compute='_get_last_status')
    x_calendar_attendance_id = fields.Many2one('resource.calendar.fto.attendance', string="Calendar Attendance ID")
    #x_holiday_ids = fields.Many2many('hr.holidays', 'fto_hr_holiday_rel', '', '' string="Holidays")

    @api.constrains('x_hours_from', 'x_hours_to', 'x_employee_id', 'x_hours_billable')
    def _check_validity(self):
        for r in self:
            # verifies if Billable Hours is between 0-16
            if r.x_hours_billable and r.x_hours_billable > 16 or r.x_hours_billable < 0:
                raise exceptions.ValidationError(_('Enter Billable Hours Between 0-16.'))

            # we take the latest shift before our x_hours_from time and check it doesn't overlap with ours
            last_shift = self.env['hr.shift.schedule'].search([
                ('x_employee_id', '=', r.x_employee_id.id),
                ('x_hours_from', '<=', r.x_hours_from),
                ('id', '!=', r.id),
            ], order='x_hours_from desc', limit=1)
            if last_shift.x_hours_from:
                date1 = r.x_hours_from.split()
                date2 = last_shift.x_hours_from.split()
                if date1[0] == date2[0] and r. x_shift_type.x_name != 'Split': # Limit one shift record per “Work From” day UNLESS shift type = Split, then 2 records per “Work From”
                    raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                        'empl_name': r.x_employee_id.name,
                        'datetime': fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(r.x_hours_from))),
                    })
            else:
                last_shift = self.env['hr.shift.schedule'].search([
                    ('x_employee_id', '=', r.x_employee_id.id),
                    ('x_hours_from', '>=', r.x_hours_from),
                    ('id', '!=', r.id),
                ], order='x_hours_from desc', limit=1)
                if last_shift.x_hours_from:
                    date1 = r.x_hours_from.split()
                    date2 = last_shift.x_hours_from.split()
                    if date1[0] == date2[0] and r. x_shift_type.x_name != 'Split':
                        raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                            'empl_name': r.x_employee_id.name,
                            'datetime': fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(r.x_hours_from))),
                        })

            # verifies if Work To is earlier than Work From.
            if r.x_hours_from and r.x_hours_from > r.x_hours_to:
                raise exceptions.ValidationError(_('"Work To" time cannot be earlier than "Work From" time.'))

            # verifies if Work from not exceed 24 hours
            _from = datetime.strptime(r.x_hours_from, '%Y-%m-%d %H:%M:%S')
            _to = datetime.strptime(r.x_hours_to, '%Y-%m-%d %H:%M:%S')
            time_delta = (_to - _from)
            total_hours = time_delta.total_seconds()
            if total_hours > 86400:
                raise exceptions.ValidationError(_('"Work To" time cannot be more than 24 hours from "Work From" time.'))

    @api.depends('x_employee_id', 'x_hours_from')
    def _get_last_status(self):
        for r in self:
            if r.x_employee_id:
                # Catch the schedule within the same day
                date = r.x_hours_from.split()
                date1 = date[0] + " 00:00:00"
                date2 = date[0] + " 23:59:59"
                r.last_status = self.env['hr.attendance'].search([
                    ('employee_id', '=', r.x_employee_id.id),
                    ('check_in', '>=', date1),
                    ('check_in', '<=', date2)
                ], order="check_in desc, id desc", limit=1).x_status_id.x_name

    @api.onchange('x_employee_id')
    def _onchange_employee(self):
        res = {}
        if self.x_employee_id:
            res['domain']={'x_department_id':[('id', '=', self.x_employee_id.department_id.id)]}
        else:
            res['domain']={'x_department_id':[('active', '=', True)]}
        return res

    @api.onchange('x_department_id')
    def _onchange_department(self):
        res = {}
        if self.x_department_id:
            res['domain']={'x_employee_id':[('department_id', '=', self.x_department_id.id)]}
        else:   
            res['domain']={'x_department_id':[('active', '=', True)]}
        return res

    @api.onchange('id')
    def _onchange_edit(self):
        if self.x_employee_id is not None:
            self.x_department_id = self.x_employee_id.department_id.id

    @api.model
    def create(self, vals):

        # override create method for hr_shift_schedule
        res = super(HrSchedule, self).create(vals)

        date_from = datetime.strptime(vals['x_hours_from'], '%Y-%m-%d %H:%M:%S').date()
        x_employee_name = self.env['hr.employee'].search([('id', '=', vals['x_employee_id'])]).name
        x_calendar_attendance_id = None
        resource_calendar = self.env['resource.calendar'].search(
            [('name', '=', x_employee_name)])

        #When a shift is qcreated, look for the respective resource_calendar_fto_attendance record 
        #with the same date as the "from" date within hr_shift_schedule, 
        #if it does not exist, create the record.
        result = self.env['resource.calendar.fto.attendance'].search(
            [('attendance_date', '=', date_from),('calendar_id', '=', resource_calendar.id)])

        if not result:
            rec = self.env['resource.calendar.fto.attendance'].create({
                    'calendar_id': resource_calendar.id,
                    'attendance_date': date_from,
                    'shift_id': res.id
                })
            x_calendar_attendance_id = rec.id
        else:
            result.write({'shift_id': res.id})
            x_calendar_attendance_id = result.id

        vals['x_calendar_attendance_id'] = x_calendar_attendance_id

        # execute the default method
        return res

    """@api.onchange('start_date', 'end_date')
                def get_department(self):
                    #Adding domain to  the hr_shift field
                    hr_department = None
                    if self.start_date:
                        hr_department = self.rel_hr_schedule.department_id.id
                    return {
                        'domain': {
                            'hr_shift': [('hr_department', '=', hr_department)]
                        }
                    }

    @api.multi
    def write(self, vals):
        #self._check_overlap(vals)
        return super(HrSchedule, self).write(vals)

    @api.model
    def create(self, vals):
        #self._check_overlap(vals)
        return super(HrSchedule, self).create(vals)

    def _check_overlap(self, vals):
        if vals.get('x_hours_from', False) and vals.get('x_hours_to', False):
            shifts = self.env['hr.shift.schedule'].search([('rel_hr_schedule', '=', vals.get('rel_hr_schedule'))])
            for each in shifts:
                if each != shifts[-1]:
                    if each.x_hours_to >= vals.get('x_hours_from') or each.x_hours_from >= vals.get('x_hours_from'):
                        raise Warning(_('The dates may not overlap with one another.'))
            if vals.get('x_hours_from') > vals.get('x_hours_to'):
                raise Warning(_('Work From should be less than Work To.'))
        return True"""


class HrShiftType(models.Model):
    _name = 'hr.shift.schedule.type'

    x_name = fields.Char(string="Shift Type", required=True)
    x_description = fields.Text(string="Description")