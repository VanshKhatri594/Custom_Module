from odoo import models,fields,api
from odoo.api import ValuesType, Self, readonly


class SaleRma(models.Model):
    _name='sale.rma'
    _description = 'Sale Rma'
    _rec_name = 'team_id'

    seq = fields.Char(string='RMA ID',default='New',readonly=True)
    team_id = fields.Many2one('rma.team',string='Team',required=True)
    date = fields.Date(string='Date',default=fields.Date.today)
    sale_order = fields.Many2one('sale.order',string='Sale Order')

    rma_line_ids = fields.One2many('sale.rma.line','rma_line_id',string='RMA Lines')

    @api.onchange('sale_order')
    def onchange_sale_order(self):
        if self.sale_order:
            rma_lines = []
            rma_lines = [(5, 0, 0)]
            for line in self.sale_order.order_line:
                rma_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'qty': line.product_uom_qty,
                    'price': line.price_unit,
                }))
            self.rma_line_ids = rma_lines

    @api.model_create_multi
    def create(self, vals_list):
        for rec in vals_list:
            team_id = rec.get('team_id')
            if team_id:
                team = self.env['rma.team'].browse(team_id)
                prefix = team.prefix
                seq_name = f'Sale RMA {team.name}'
                seq_code = f'sale.rma.{team.id}'

                if not self.env['ir.sequence'].search([('code', '=', seq_code)], limit=1):
                    self.env['ir.sequence'].create({
                        'name': seq_name,
                        'code': seq_code,
                        'prefix': prefix,
                        'padding': 4,
                    })

                rec['seq'] = self.env['ir.sequence'].next_by_code(seq_code)
        return super(SaleRma, self).create(vals_list)

