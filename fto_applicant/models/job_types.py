# -*- coding: utf-8 -*-

from flectra import models, fields, api

class JobTypes(models.Model):
    
    """
    This method is being defined to ensure the Flectra environment contains all the existing 
    Recruitment/Job information from the old system. This will be leveraging the existing hr.job model.
    We can use this in combination with the other custom fields created in job_other_details.py 
    to track the name of the job type.
    """
    
    _name = 'hr.job.type'

    
    # id = fields.Integer('ID',readonly=True,required=True)
    x_name = fields.Char(string='Job Type')  
