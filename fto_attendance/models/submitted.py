from flectra import models, fields, api, tools
import logging


# FLE-46
class Submitted(models.Model):
    _name = 'hr.attendance.submitted'
    _description = 'Sql view for displaying/querying employee submitted applications'
    _auto = False

    employee_id = fields.Many2one('hr.employee', string='Employee')
    user_id = fields.Many2one('res.users', string='User')

    employee_name = fields.Char('Employee Name')
    department_name = fields.Char('Department')
    check_in = fields.Char('Date')
    check_out = fields.Char('Date')
    attendance_type = fields.Char('Attendance Type')
    attendance_schedule = fields.Char('Attendance Schedule')
    shift_schedule = fields.Char('Shift Schedule')
    application_schedule = fields.Char('Application Schedule')
    status = fields.Char('Status')


    def init(self):
        tools.sql.drop_view_if_exists(self.env.cr, 'hr_attendance_submitted')
        self.env.cr.execute('''
              CREATE OR REPLACE VIEW hr_attendance_submitted AS (
              SELECT
              ROW_NUMBER () OVER ( ORDER BY hr_attendance.id ) AS id,
              hr_employee.id as employee_id,
              hr_employee.id as user_id,
              hr_employee.name AS employee_name,
              hr_department.name AS department_name,
              hr_attendance.check_in::date,
              hr_attendance.check_out::date,
              hr_shift_schedule.x_hours_from || ' - ' || hr_shift_schedule.x_hours_to AS shift_schedule,
              hr_attendance.check_in || '-' || hr_attendance.check_out AS attendance_schedule,
              hr_attendance.check_in || '-' || hr_attendance.check_out AS application_schedule,
              hr_attendance_tracking.x_name as tracking,
              hr_shift_schedule_type.x_name as attendance_type,
              hr_attendance_status.x_name as status
             FROM
               hr_attendance
             LEFT JOIN hr_employee ON hr_employee.id = hr_attendance.employee_id             
             LEFT JOIN hr_shift_schedule ON hr_shift_schedule.x_employee_id = hr_attendance.employee_id
             LEFT JOIN hr_department ON hr_department.id = hr_shift_schedule.x_department_id
             LEFT JOIN hr_shift_schedule_type ON hr_shift_schedule_type.id = hr_attendance.x_type_id
             LEFT JOIN hr_attendance_tracking ON hr_attendance_tracking.id = hr_attendance.x_tracking_id
             LEFT JOIN hr_attendance_type ON hr_attendance_type.id = hr_attendance.x_type_id
             LEFT JOIN hr_attendance_status ON hr_attendance_status.id = hr_attendance.x_status_id
             );
           ''')

submitted = Submitted()

