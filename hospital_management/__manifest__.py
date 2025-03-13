# -*- coding: utf-8 -*-
{
    'name': 'Hospital Management',
    'description': 'Hospital Management System',
    'author': 'Vansh Khatri',
    'depends': ['base'],
    'sequence': 1,
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/patient_view.xml',
        'views/appointments_view.xml',
    ],
}
