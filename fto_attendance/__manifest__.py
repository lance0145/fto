# -*- coding: utf-8 -*-
{
    'name': "fto_attendance",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','hr_attendance','resource','fto_shift_management'],

    # always loaded
    'data': [
        'views/fto_application_center.xml',
        'views/automation.xml',
        'data/fto_attendance_status_initial_records.xml',
        'data/fto_attendance_tracking_initial_records.xml',
        'data/fto_attendance_type_initial_records.xml',
    ],
    
     
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': True,

}
