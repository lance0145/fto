from flectra import models, fields, api

class JobAssessmentSurveyRelation(models.Model):
    """
    In the following method we define FTO Custom fields that will be leveraging
    with hr.job module. Here is where we will create survey_id's to be associated 
    as "Assessments" for a Job Position. We create surveyID and JobID so that the 
    "Assessments" can be linked to a certain job.
    """
    
    
    _name = 'fto_hr_job_survey_rel'
    _description = 'A relation/table that will hold id of jobs with a corresponding survey id'

    job_id = fields.Integer('Job Id')
    survey_id = fields.Integer('Survey Id')
