# -*- coding: utf-8 -*-
{
    'name': "fto_shift_management",

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
    'depends': [
        "hr", 
        "hr_payroll", 
        "resource",
    ],

    # always loaded
    'data': [
        #"security/ir.model.access.csv", 
        #"security/hr_employee_shift_security.xml", 
        "views/hr_employee_shift_view.xml", 
        "views/hr_employee_contract_view.xml", 
        "views/hr_generate_shift_view.xml",
        "views/fto_shift_schedule.xml", 
        "views/templates.xml",
        "data/fto_shift_type_initial_record.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
       'demo/demo.xml',
    ],
    
    'installable': True,
    # 'auto_install': False,
    'application': True,
}

