from odoo import models, fields

class Teacher(models.Model):
    _name = 'teacher.details'
    _description = 'Teacher'

    name = fields.Char(string="Teacher Name", required=True)
    contact = fields.Char(string="Contact")
    teacher_id = fields.Char(string="Teacher Id")
    salary = fields.Float(string="Salary")

    school_name = fields.Many2one('school.details', string='School Name')



