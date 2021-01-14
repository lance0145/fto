# Copyright (C) 2020 Fair Trade Outsourcing
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "FTO Survey",
    'version': '1.0.1.0.0',
    'license': 'AGPL-3',
    'author': ""
               "Fair Trade Outsourcing",
    "website": "https://gitlab.com/flectra-community/hr",
    "category": "Survey",
    "summary": "Compute Maximum score for the quiz and Score Percentage",
    "depends": [
        "survey","hr_recruitment_survey"
    ],
    "data": [
        'views/fto_survey.xml',
        'data/fto_survey_type_data.xml'
    ],
    'installable': True,
    # 'auto_install': False,
    'application': True,
}
