from odoo import fields,models,api


class StockMove(models.Model):
    _inherit = 'stock.move'

    prescription_line_id = fields.Many2one('prescription_line.details','Prescription Line')
