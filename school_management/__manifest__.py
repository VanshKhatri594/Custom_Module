# -*- coding: utf-8 -*-
{
    'name': 'School Management',
    'description': 'Manage Schools',
    'author': 'Vansh Khatri',
    'depends': ['base'],
    'sequence': 1,
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'views/school_view.xml',
    ],
}

