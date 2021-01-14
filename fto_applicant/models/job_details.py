# -*- coding: utf-8 -*-

from flectra import models, fields, api

class JobDetails(models.Model):
    
    """
    This method is being defined to ensure the Flectra environment contains all the existing 
    Recruitment/Job information from the old system. This will be leveraging the existing hr.job model.
    We will create the following custom fields to extend on the model: vacancy_urgent, vacancy_internship,
    vacany_seasonal, salary_estimated, and job_type_id.
    """
    
    _inherit = ['hr.job']

    x_vacancy_urgent = fields.Integer('Urgent Vacancy')
    x_vacancy_internship = fields.Integer('Internship Vacancy')
    x_vacancy_seasonal  = fields.Integer('Seasonal Vacancy')
    x_salary_estimated = fields.Integer('Estimated Salary')
    x_job_type_id = fields.Many2one('hr.job.type',ondelete='set null', string="Job Type")
    x_branch_id = fields.Many2one('res.branch',ondelete='set null', string="Branch")
    x_job_assessment_ids = fields.Many2many('survey.survey','fto_hr_job_survey_rel','job_id','survey_id',string='Assessments')
    