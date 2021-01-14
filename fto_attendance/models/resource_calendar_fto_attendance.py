# -*- coding: utf-8 -*-

from flectra import models, fields, api, _
from flectra.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta
import logging
import time

_logger = logging.getLogger(__name__)


class ResourceCalendarFTOattendance(models.Model):
    _name = "resource.calendar.fto.attendance"

    calendar_id = fields.Many2one('resource.calendar', string="Application Time", required=True)
    attendance_date = fields.Date(string="Attendance Date", required=True)
    attendance_ids = fields.One2many('hr.attendance','x_calendar_attendance_id', string="Attendance/s")
    check_in = fields.Datetime(string="Check In", default=None)
    check_out = fields.Datetime(string="Check Out", default=None)
    overtime_hours = fields.Float(string="Overtime Hours")
    device_id = fields.Char(string='Biometric Device ID')
    company_id = fields.Char(related="calendar_id.x_employee_id.company_id.name")
    tracking_id = fields.Many2one("hr.attendance.tracking", string="Tracking Type")
    type_id = fields.Many2one("hr.attendance.type", string="Attendance Type")
    shift_id = fields.Many2one("hr.shift.schedule", string="Schedule")
    shift_from = fields.Datetime(related="shift_id.x_hours_from",store=True, tracking=True)
    shift_to = fields.Datetime(related="shift_id.x_hours_to",store=True, tracking=True)

class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    x_employee_id = fields.Many2one('hr.employee', 'Employee')
    x_calendar_attendance_id = fields.One2many('resource.calendar.fto.attendance', 'calendar_id')


class HREmployees(models.Model):
    _inherit = ['hr.employee']

    x_calendar_id = fields.Many2one('resource.calendar', string='Resource Calendar')

    @api.model_cr
    def init(self):
        self.env.cr.execute("SELECT id, name, company_id FROM hr_employee"
                   " WHERE active = True"
                   "   AND x_calendar_id IS NULL")
        for uid, name, company_id in self.env.cr.fetchall():
            self.sudo()._create_resource_calendar_record(name,company_id,uid)

    # override create method for employee
    @api.model
    def create(self, vals):
        # execute the default method
        res = super(HREmployees, self).create(vals)
        
        #create a record of employee in resource_calendar
        company_id = self.company_id and self.company_id.id or self.department_id.company_id.id
        self.sudo()._create_resource_calendar_record(vals['name'],company_id,res.id)        

        return res

    def _create_resource_calendar_record(self, name, company_id, employee_id):
        if employee_id:
            result = self.env['resource.calendar'].search([('name', '=', name)])

            if not result:
                resource_calendar = self.env['resource.calendar'].create({
                        'name': name,
                        'company_id': company_id,
                        'tz': 'Asia/Manila',
                        'x_employee_id': employee_id,
                    })

                self.sudo()._create_resource_calendar_fto_attendance_record(resource_calendar.id)
                
                #update employee_ide record set x_calendar_id
                self.sudo().browse(resource_calendar.id)._set_calendar_id(employee_id)

    def _set_calendar_id(self,employee_id):
        self.env.cr.execute(
            "UPDATE hr_employee SET x_calendar_id=%s WHERE id=%s",
            (self.id,employee_id))

    def _create_resource_calendar_fto_attendance_record(self, calendar_id):
        # pre-populate blank rows for each ACTIVE employee and their respective calendar (hr_employee.x_calendar_id), 30 days in advance
        counter = 1
        while counter <= 30:
            attendance_date = date.today() + timedelta(counter)
            res = self.env['resource.calendar.fto.attendance'].create({
                    'calendar_id': calendar_id,
                    'attendance_date': attendance_date,
                })

            counter += 1



#This is just to fix the error in zk_machine_attendance when installing the modules
# class HREmployeesInheritZK(models.Model):
#     _inherit = ['zk.machine.attendance']

#     x_calendar_attendance_id = fields.One2many('resource.calendar.fto.attendance', 'calendar_id')