# -*- coding: utf-8 -*-
# Developer : Allan Abendanio
# Date : 30-Oct-2020
# HR - Attendance - Custom Model - Approval, Tracking, Type & Status

from flectra import models, fields, api
from datetime import date, datetime, timedelta
import logging
import time
from datetime import date, datetime, timedelta

_logger = logging.getLogger(__name__)


class Tracking(models.Model):
    _name = 'hr.attendance.tracking'
    x_name = fields.Char(string="Tracking", required=True)
    x_description = fields.Char(string='Description')


class Type(models.Model):
    _name = 'hr.attendance.type'
    x_name = fields.Char(string="Type", required=True)
    x_description = fields.Char(string='Description')


class Status(models.Model):
    _name = 'hr.attendance.status'
    x_name = fields.Char(string="Status", required=True)
    x_description = fields.Char(string='Description')

class Attendance(models.Model):
    _inherit = ['hr.attendance']

    # _default_tracking
    @api.model
    def _default_tracking(self):
        return self.env['hr.attendance.tracking'].search([('x_name','!=','BioMetrics')], limit=1)

    # _default_status
    @api.model
    def _default_status(self):
        return self.env['hr.attendance.status'].search([('x_name','=','Pending')], limit=1)

    # logic #4 of Overall Form, default hr.attendance.x_type_id = Attendance
    @api.model
    def _default_type(self):
        return self.env['hr.attendance.type'].search([('x_name','=','Attendance')], limit=1)

    # logic #1 of CoA Applications, display the Employee of the user submitting an Application
    @api.returns('self')
    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)])

    x_tracking_id = fields.Many2one('hr.attendance.tracking', string='Attendance Tracking', default=_default_tracking)
    x_type_id = fields.Many2one('hr.attendance.type', string='Attendance Type', default=_default_type)
    x_status_id = fields.Many2one('hr.attendance.status', string='Attendance Status', default=_default_status)
    x_approved_by = fields.Many2one('res.partner', string='Approved By')
    x_rejected_by = fields.Many2one('res.partner', string='Rejected By')
    employee_id = fields.Many2one('hr.employee', string='Employee', default=_default_employee)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.uid)
    check_in = fields.Datetime(string="Check In")
    check_out = fields.Datetime(string="Check Out")
    company_id = fields.Many2one('res.company', string='Company')
    department_id = fields.Many2one('hr.department', string='Department')
    shift_ids = fields.Many2many('hr.shift.schedule')
    # tree view for employee schedule for new model
    #x_calendar_attendance_ids = fields.Many2many('resource.calendar.fto.attendance')
    x_calendar_attendance_id = fields.Many2one('resource.calendar.fto.attendance')
    x_approved_date = fields.Datetime(string="Approved Date")
    
    approved_count = fields.Integer(string='Approved', compute='approved_application_count')
    rejected_count = fields.Integer(string='Rejected', compute='rejected_application_count')
    cancelled_count = fields.Integer(string='Cancelled', compute='cancelled_application_count')
    pending_count = fields.Integer(string='Pending', compute='pending_application_count')

    shift_schedule = fields.Char(string='Shift Schedule', compute='_get_shift_schedule')
    attendance_schedule = fields.Char(string='Attendance Schedule', compute='_get_attendance_schedule')
    application_schedule = fields.Char(string='Application Schedule', compute='_get_application_schedule')

    @api.depends('check_in', 'employee_id')
    def _get_shift_schedule(self):
        for r in self:
            if r.check_in:
                date = r.check_in.split()
                date1 = date[0] + " 00:00:00"
                date2 = date[0] + " 23:59:59"
                shift = self.env['hr.shift.schedule'].search([
                    ('x_employee_id', '=', r.employee_id.id),
                    ('x_hours_from', '>=', date1),
                    ('x_hours_from', '<=', date2)
                ], order="x_hours_from desc, id desc", limit=1)
                if shift.x_hours_from:
                    _from = datetime.strptime(shift.x_hours_from, '%Y-%m-%d %H:%M:%S')
                    _to = datetime.strptime(shift.x_hours_to, '%Y-%m-%d %H:%M:%S')
                    time_delta = (_to - _from)
                    total_hours = time_delta.total_seconds()
                    r.shift_schedule = "{}".format(str(timedelta(seconds=total_hours)))

    @api.depends('check_in', 'check_out', 'x_type_id', 'x_status_id')
    def _get_attendance_schedule(self):
        for r in self:
            if r.check_in and r.x_type_id.x_name == 'Attendance' and r.x_status_id.x_name == 'Approved':
                _from = datetime.strptime(r.check_in, '%Y-%m-%d %H:%M:%S')
                _to = datetime.strptime(r.check_out, '%Y-%m-%d %H:%M:%S')
                time_delta = (_to - _from)
                total_hours = time_delta.total_seconds()
                r.attendance_schedule = "{}".format(str(timedelta(seconds=total_hours)))

    @api.depends('check_in', 'check_out')
    def _get_application_schedule(self):
        for r in self:
            if r.check_in:
                _from = datetime.strptime(r.check_in, '%Y-%m-%d %H:%M:%S')
                _to = datetime.strptime(r.check_out, '%Y-%m-%d %H:%M:%S')
                time_delta = (_to - _from)
                total_hours = time_delta.total_seconds()
                r.application_schedule = "{}".format(str(timedelta(seconds=total_hours)))

    @api.depends('employee_id')
    def approved_application_count(self):
        count = self.env['hr.attendance'].search_count([('x_status_id', '=', 2), (
            'employee_id', '=', self.env['hr.employee'].search([('user_id', '=', self.env.uid)]).id)])
        self.approved_count = count

    @api.depends('employee_id')
    def rejected_application_count(self):
        count = self.env['hr.attendance'].search_count([('x_status_id', '=', 4), (
            'employee_id', '=', self.env['hr.employee'].search([('user_id', '=', self.env.uid)]).id)])
        self.rejected_count = count

    @api.depends('employee_id')
    def cancelled_application_count(self):
        count = self.env['hr.attendance'].search_count([('x_status_id', '=', 3), (
            'employee_id', '=', self.env['hr.employee'].search([('user_id', '=', self.env.uid)]).id)])
        self.cancelled_count = count

    @api.depends('employee_id')
    def pending_application_count(self):
        count = self.env['hr.attendance'].search_count([('x_status_id', '=', 1), (
            'employee_id', '=', self.env['hr.employee'].search([('user_id', '=', self.env.uid)]).id)])
        self.pending_count = count


    """Verify if the user submitting has elevated privileges as a manager so that the record being created is automatically 
        set to hr.attendance.x_status_id of APPROVED. Application submissions from users without elevated privileges need 
        to be set to hr.attendance.x_status_id of PENDING."""

    @api.model
    def create(self, vals):
        # execute the default method
        res = super(Attendance, self).create(vals)
        # probe user level
        is_manager = self.env['hr.employee'].search([('user_id', '=', self.env.uid)]).manager
        is_attendance_manager = self.env['res.users'].search([('id', '=', self.env.uid),('groups_id.name', '=', 'Manager'),('groups_id.category_id.name', '=', 'Attendance')])
        
        approved_id = self.env['hr.attendance.status'].search([('x_name','=','Approved')], limit=1)
        
        if (is_manager or is_attendance_manager):
            vals['x_status_id'] = approved_id.id
            res.write({'x_status_id': approved_id.id})

        return res


    # logic #3 & 4 of CoA Applications, display the companies the selected Employee's
    # default to the "default company" mapped to a particular User/Employee
    @api.onchange('employee_id')
    def onchange_employee_details(self):

        # update/refressh/unlink shift_ids tree view
        res = {
            'value': {
                #'x_calendar_attendance_ids': [(2, x,) for x in self.x_calendar_attendance_ids.ids],
                'shift_ids': [(2, x,) for x in self.shift_ids.ids],
            }
        }
        for r in self:
            if r.employee_id:
                r.company_id = r.employee_id.company_id.id
                r.department_id = r.employee_id.department_id.id
                # onchange one2many list view of schedule
                r.shift_ids = self.env['hr.shift.schedule'].search([('x_employee_id', '=', r.employee_id.id)]).ids
                #r.x_calendar_attendance_ids = self.env['resource.calendar.fto.attendance'].search([('calendar_id.x_employee_id', '=', r.employee_id.id),('shift_id', '!=', False)]).ids

        return res

    # catch the user who Approve or Reject the Application.
    @api.onchange('x_status_id')
    def set_modifier(self):
        if self.x_status_id.x_name == "Approved":
            self.x_approved_by = self.user_id
        elif self.x_status_id.x_name == "Rejected":
            self.x_rejected_by = self.user_id

    # Note: logic #1 & 2 of Overall Form, has built-in logic already existing on module hr_attendance
    # logic #5 of Overall Form, Display confirmation(code is in view), this code will clear the form
    @api.model
    def submit_application(self, vals):
        # update the last_status of hr.shift.schedule of the employee
        # for r in self:
        #   if r.employee_id:
        #       date = r.r.check_in()
        #       date2 = date[0] + " 23:59:59"
        #       employee_schedule = self.env['hr.shift.schedule'].search([('x_employee_id', '=', r.employee_id.id), ('x_hours_from', '>=', r.check_in), ('x_hours_from', '<=', date2)], order="x_hours_from desc, id desc", limit=1)
        #       employee_schedule.update({'last_status': vals['x_status_id']})
        #       break
        return {
                'type': 'ir.actions.client',
                'tag': 'reload',
        }


    # override write method for hr_attendance
    @api.multi
    def write(self, vals):
        type_attendance = self.env['hr.attendance.type'].search([('x_name','=','Attendance')], limit=1).id
        type_overtime = self.env['hr.attendance.type'].search([('x_name','=','Overtime')], limit=1).id
        type_restday = self.env['hr.attendance.type'].search([('x_name','=','Rest Day')], limit=1).id
        type_leave = self.env['hr.attendance.type'].search([('x_name','=','Leave Request')], limit=1).id


        date_from = datetime.strptime(self.check_in, '%Y-%m-%d %H:%M:%S').date()
        resource_calendar = self.env['resource.calendar'].search(
            [('name', '=', self.employee_id.name)])
        result = self.env['resource.calendar.fto.attendance'].search(
            [('attendance_date', '=', date_from),('calendar_id', '=', resource_calendar.id)])

        if result:
            #set the x_calendar_attendance_id
            vals['x_calendar_attendance_id'] = result.id
            x_status_id_name = self.env['hr.attendance.status'].search([('id','=',vals['x_status_id'])]).x_name
            #When an hr_attendance_type = "Attendance" application is "Approved", 
            #need to trigger a function that updates the respective resource_calendar_fto_attendance 
            #record for that particular day with the "check_in" and "check_out" times.
            if self.x_type_id.id == type_attendance and x_status_id_name == "Approved":
                result.write({'check_in': self.check_in, 'check_out': self.check_out})

            #When an hr_attendance_type = "Overtime" application is "Approved", 
            #need to trigger a function that updates the respective resource_calendar_fto_attendance 
            #record for that particular day with the "overtime_hours" value.
            if self.x_type_id.id == type_overtime and x_status_id_name == "Approved":
                check_out = datetime.strptime(self.check_out, '%Y-%m-%d %H:%M:%S')
                check_in = datetime.strptime(self.check_in, '%Y-%m-%d %H:%M:%S')
                time_delta = (check_out - check_in)
                total_seconds = time_delta.total_seconds()
                overtime_minutes = total_seconds/60
                result.write({'overtime_hours': overtime_minutes})

            #When an hr_attendance_type = "Leave Request" application is "Approved", 
            #need to trigger a function that updates hr_shift_schedule for that particular day, 
            #clearing out any pre-loaded shift ranges and updating associated hr_shift_schedule_type = "Leave".
            if self.x_type_id.id == type_leave and x_status_id_name == "Approved":
                hr_shift_schedule_type_leave = self.env['hr.shift.schedule.type'].search([('x_name','=','Leave')], limit=1)
                hr_shift_schedule_res = self.env['hr.shift.schedule'].search(
                    [('x_calendar_attendance_id', '=', result.id)])

                hr_shift_schedule_res.write({'x_shift_type': hr_shift_schedule_type_leave.id})

            #When an hr_attendance_type = "Rest Day" application is "Approved", 
            #need to trigger a function that updates hr_shift_schedule for that particular day, 
            #replacing any pre-loaded with a default datetime for the day submitted and updating associated hr_shift_schedule_type = "Rest Day".
            if self.x_type_id.id == type_restday and x_status_id_name == "Approved":
                hr_shift_schedule_type_leave = self.env['hr.shift.schedule.type'].search([('x_name','=','Rest Day')], limit=1)
                hr_shift_schedule_res = self.env['hr.shift.schedule'].search(
                    [('x_calendar_attendance_id', '=', result.id)])

                hr_shift_schedule_res.write({'x_shift_type': hr_shift_schedule_type_leave.id})


        # execute the default method
        res = super(Attendance, self).write(vals)
        return res

    # action to show dialog form    
    @api.multi
    def show_dialog(self,context):  

        if self.id:
            return{
                'type':'ir.actions.act_window',
                'name':'Confirmation',
                'res_model':'hr.attendance',
                'view_type':'form',
                'view_mode':'form',
                'target':'new',
                'res_id': self.id           
            }
        else:
            return{
                'type':'ir.actions.act_window',
                'name':'Confirmation',
                'res_model':'hr.attendance',
                'view_type':'form',
                'view_mode':'form',
                'target':'new',
                'res_id': self.env.uid
            }
        

    # action to cancel application  
    def action_cancel(self):                
        records = self.env['hr.attendance'].browse(self._context.get('active_ids'))
        for record in records:
            self.env.cr.execute('UPDATE hr_attendance SET x_status_id=3 WHERE id =' + str(record.id))
        # remove entry that has no check_out
        self.env.cr.execute('DELETE FROM hr_attendance WHERE check_out IS NULL')
        