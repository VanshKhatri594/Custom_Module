from odoo import models,fields,api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    extra_discount = fields.Float(string='Extra Discount',default=0.1)
    use_customers_tc = fields.Boolean(string='Customers T&C')
    terms_and_conditions = fields.Text(string='Terms and Conditions')






