from odoo import fields,models,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    previous_price = fields.Float(compute='_compute_previous_price', string="Previous Price")

    # inherited method or override
    @api.depends('product_id', 'product_uom', 'product_uom_qty','order_partner_id.extra_discount')
    def _compute_discount(self):
        res = super(SaleOrderLine, self)._compute_discount()
        for order in self:
            order.discount += order.order_partner_id.extra_discount
        return res

    # created our own method
    @api.depends('product_template_id')
    def _compute_previous_price(self):
        for rec in self:
            rec.previous_price = rec.product_id.lst_price
