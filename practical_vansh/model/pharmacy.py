from odoo import fields,models,api
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _name = 'sale.pharmacy'
    _description = 'Pharmacy'

    name = fields.Char(string='Name')




