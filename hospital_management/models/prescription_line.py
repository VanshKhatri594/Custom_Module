from email.policy import default

from odoo import fields, models, api
from odoo.api import constrains
from odoo.fields import first
from odoo.exceptions import ValidationError

class PrescriptionLine(models.Model):
    _name = 'prescription_line.details'
    _description = 'Prescription Line Information'
    _rec_name = 'product_id'

    # product.product -> Product Variants
    product_id = fields.Many2one('product.product',string='Product',required=True)
    qty = fields.Integer(string='Quantity',default=1,required=True)
    price_unit = fields.Float(string='Unit Price')
    total = fields.Float(string='Total',compute='_compute_total',store=True)
    prescription_id = fields.Many2one('prescription_details','Prescription')
    move_ids = fields.One2many('stock.move','prescription_line_id',string='Prescriptions')
    delivered_qty = fields.Integer(compute='_compute_delivered_qty',string='Delivery Count',store=True)
    remaining_qty = fields.Integer(compute='_compute_remaining_qty',string='Remaining Qty')

    @api.constrains('qty')
    def check_quantity(self):
        for rec in self:
            qty_in_move = sum(rec.move_ids.mapped('product_uom_qty'))
            if rec.qty < qty_in_move:
                raise ValidationError("Quantity in prescription cannot be less than quantity in stock move.")

    @api.depends('qty', 'price_unit')
    def _compute_total(self):
        for record in self:
            record.total = record.qty * record.price_unit

    @api.depends('move_ids.state', 'move_ids.product_uom_qty', 'move_ids.quantity')
    def _compute_delivered_qty(self):
        for rec in self:
            rec.delivered_qty = sum(rec.move_ids.filtered(lambda s: s.state == 'done').mapped('quantity'))
            print(rec.delivered_qty)

    @api.depends('move_ids.quantity','move_ids.state','move_ids.product_uom_qty')
    def _compute_remaining_qty(self):
        for rec in self:
            qty_in_move = sum(rec.move_ids.mapped('product_uom_qty'))
            rec.remaining_qty = qty_in_move - rec.delivered_qty




