from email.policy import default

from odoo import models,fields,api


class RmaTeam(models.Model):
    _name = 'rma.team'
    _description = 'RMA Team'

    name = fields.Char(string='Team Name')
    prefix = fields.Char(string='Prefix')
