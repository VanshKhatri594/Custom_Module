from odoo import models,fields,api


class AddDocumentsWizard(models.TransientModel):
    _name = 'add.documents.wizard'
    _description = 'Wizard'

    sale_id = fields.Many2one('sale.order',string='Sale Order')
    product_ids = fields.Many2many('product.product',string='Products')

    def add_docs(self):
        self.sale_id = self._context.get('active_id')
        sale_lines = []
        for product in self.product_ids:
            if product:
                sale_lines.append((0,0,{
                    'product_id':product.id,
                    'product_uom_qty':1,
                }))
        self.sale_id.order_line = sale_lines



