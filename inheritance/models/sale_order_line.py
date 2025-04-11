from odoo import fields,models,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    previous_price = fields.Float(compute='_compute_previous_price', string="Previous Price")
    location_ids = fields.Many2many("stock.location", string="Locations")
    quantity_available_at_locations = fields.Float(string="Available Quantity at location",
                                                   compute="_compute_quantities")
    quantity_available_at_wh = fields.Float(string="Available Quantity at Warehouse",
                                            compute="_compute_quantities")

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

    # @api.depends('order_id.warehouse_id', 'product_id', 'location_ids')
    def _compute_quantities(self):
        for rec in self:
            rec.quantity_available_at_locations = rec.product_id.with_context(location=rec.location_ids.ids).qty_available
            rec.quantity_available_at_wh = rec.product_id.with_context(warehouse_id=rec.order_id.warehouse_id.id).qty_available
