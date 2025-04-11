# -*- coding: utf-8 -*-
{
    'name': 'RMA',
    'description': 'Return Merchandise Authorization',
    'author': 'Vansh Khatri',
    'depends': ['base','sale'],
    'sequence': 1,
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'views/sale_rma_view.xml',
        'views/rma_team_view.xml',
    ],
}
