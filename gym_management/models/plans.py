from odoo import models, fields

class GymPlan(models.Model):
    _name = 'gym.plans'
    _description = 'Gym Membership Plan'

    name = fields.Char(string="Plan Name", required=True)
    plan_type = fields.Selection([
        ('basic', 'Basic'),
        ('premium', 'Premium')
    ], string="Plan Type", required=True, default='basic')
    price = fields.Float(string="Plan Price", required=True)
    duration = fields.Selection([
        ('1_month', '1 Month'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('12_months', '12 Months')
    ], string="Duration", required=True)
    member_ids = fields.One2many('gym.members', 'plan_id', string="Subscribed Members")
