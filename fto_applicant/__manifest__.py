# -*- coding: utf-8 -*-

#The __manifest__.py file serves to declare a python package as an Flectra module and to specify 
#module metadata. It contains a single Python dictionary, where each key specifies module metadatum.

{
    'name': "fto-applicant",

    'summary': """
        FTO Applicant hiring module
        """,

    'description': """
        Long description of module's purpose
        """,

    'author': "FTO",
    'website': "https://www.fairtradeoutsourcing.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    #FLE3 - added hr_recruitment module for views inheritance (future plans)
    'depends': ['hr_recruitment','website_form','website_hr_recruitment','contacts','survey','resource'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
        #'views/fto_res_partner_education_view.xml',
        'views/fto_identifications_view.xml',
        'views/fto_other_details_view.xml',
        'views/fto_applicant_name_inherited.xml',
        'views/fto_applicant_disqualify.xml',
        'views/fto_applicant_assessment_view.xml',
        'views/fto_applicant_job_apply.xml', 
        'views/fto_addons_menu.xml',
        'views/fto_identifications.xml',
        'views/fto_applicant_thankyou_page_assessment_view_inherited.xml',
        'views/fto_job_assessments_inhertied.xml',
        'views/fto_lnd_view.xml',
        'views/fto_fluency_capture_form_inherited.xml',
        'views/fto_job_branch_inherited.xml',
        'views/applicant_stages.xml',
        'views/fto_educations.xml',
        'views/fto_internet.xml',
        'views/fto_other_details_capture_form.xml',
        'data/fto_identifications_initial_records.xml',
        'data/config_data.xml',
        'data/fto_internet_plan_initial_records.xml',
        'data/fto_internet_provider_initial_records.xml',
        'data/fto_internet_type_initial_records.xml',
        'data/fto_education_level_options.xml',
        'data/fto_education_course_options.xml',
        'data/fto_assessment_resend_email.xml',
        'data/mail_template_data.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
        #'demo/demo.xml',
    #],

    'installable': True,
    # 'auto_install': False,
    'application': True,
}
