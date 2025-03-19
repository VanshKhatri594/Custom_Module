from odoo import fields, models, api
from odoo.api import model_create_multi


class Members(models.Model):
    _name = 'gym.members'
    _description = 'Members Information'

    member_id = fields.Char(string='ID',readonly=True)
    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    plan_id = fields.Many2one('gym.plans', string='Subscribed Plan')


    @model_create_multi
    def create(self,vals_list):
        res = super(Members,self).create(vals_list)
        for rec in res:
            rec.member_id = self.env['ir.sequence'].next_by_code('gym.members')
        return res