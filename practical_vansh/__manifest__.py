# -*- coding: utf-8 -*-
{
    'name': 'Practical Vansh',
    'description': 'Evaluation Test 2',
    'author': 'Vansh Khatri',
    'depends': ['base','sale','purchase'],
    'sequence': 1,
    'application': True,

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'data/pharmacy.xml',
        'views/pharmacy_view.xml',
        'views/sale_order_view.xml',
        'views/account_move.xml',
        'views/res_config_sett_view.xml',
        'views/deliveryslip_report.xml',
        'wizard/add_documents.xml',
    ],
}
