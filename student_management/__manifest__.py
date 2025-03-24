# -*- coding: utf-8 -*-
{
    'name': 'Student Management',
    'description': 'Student Management System',
    'author': 'Vansh Khatri',
    'depends': ['base','product'],
    'sequence': 1,
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'views/student_view.xml',
        'views/subject_view.xml',
        'views/tuition_fees_view.xml',
    ],
}
