{
    'name' : 'Gym Management',
    'author' : 'Vansh Khatri',
    'description' : 'Gym Management System',
    'depends' : ['base'],
    'sequence' : 1,
    'application' : True,


    'data' : [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/members_view.xml',
        'views/plans_view.xml',
    ],


}