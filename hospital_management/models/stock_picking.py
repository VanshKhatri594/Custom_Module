from odoo import fields,models,api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    lead_reference = fields.Char(string='Lead Reference')

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super().create()
    #     return res