from odoo import fields,models,api


class Subject(models.Model):
    _name = 'subject.subject'
    _description = 'Subject Information'

    name = fields.Char(string='Name',required=True)
