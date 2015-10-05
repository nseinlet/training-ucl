# -*- coding: utf-8 -*-
{
    'name': "../epc/",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail', 'board'],
    
    # always loaded
    'data': [
        'views/activity.xml',
        'views/activityinfo.xml',
        'views/specset.xml',
        'views/partner.xml',
        'views/entity.xml',
        'views/activityinfo_workflow.xml',
        'views/activityinfoanalysis.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'wizards/resultswizard.xml',
        'reports/activityinfo.xml',
        'reports/epcdashboard.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
