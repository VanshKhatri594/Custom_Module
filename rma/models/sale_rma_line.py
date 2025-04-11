from odoo import models,fields,api


class SaleRmaLine(models.Model):
    _name='sale.rma.line'
    _description = 'Rma Line'

    rma_line_id = fields.Many2one('sale.rma',string='Rma Line Id')
    product_id = fields.Many2one('product.product',string='Product')
    qty = fields.Float(string='Quantity')
    price = fields.Float(string='Unit Price')


