from email.policy import default

from odoo import fields,models,api


class TuitionFees(models.Model):
    _name = 'tuition.fees.structure'
    _description = 'Fees Information'
    _rec_name = 'product'

    # product.template -> Products
    product = fields.Many2one('product.template','Product',required=True)
    fees_amount = fields.Float(string='Fees Amount')

    quantity = fields.Float(string='Quantity')
    discount = fields.Float(string='Discount')
    subtotal = fields.Float(string='Sub Total',compute='on_compute_subtotal',store= True)
    total = fields.Float(string='Total',compute='on_compute_total',store=True)
    standard = fields.Selection([
        ('one', '1'),
        ('two', '2'),
        ('three', '3'),
        ('four', '4'),
        ('five', '5'),
        ('six', '6'),
        ('seven', '7'),
        ('eight', '8'),
        ('nine', '9'),
        ('ten', '10'),
        ('eleven', '11'),
        ('twelve', '12')
    ])

    @api.depends('fees_amount','quantity')
    def on_compute_subtotal(self):
        for rec in self:
            if rec.fees_amount and rec.quantity:
                rec.subtotal = rec.fees_amount * rec.quantity

    @api.depends('subtotal','discount')
    def on_compute_total(self):
        for rec in self:
            rec.total = rec.subtotal - ((rec.subtotal * rec.discount) / 100)


