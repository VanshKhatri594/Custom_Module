from odoo import models, fields


class Student(models.Model):
    _name = 'student.details'
    _description = 'Student Details'

    name = fields.Char(string='Student Name', required=True)
    enroll_no = fields.Char(string='Enrollment No', required=True)
    age = fields.Integer(string='Age')
    dob = fields.Date(string='Date of Birth')
    contact_no = fields.Char(string='Contact Number')

    school_name = fields.Many2one('school.details', string='School Name', required=True)
