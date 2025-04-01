from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Prescription(models.Model):
    _name = 'prescription_details'
    _description = 'prescription Information'
    _rec_name = 'patient_id'

    prescription_code = fields.Char(string="Id", required=True, default="New")
    patient_id = fields.Many2one('hospital.patient', string='Patient')
    date = fields.Datetime(string='Date', required=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('cancel','Cancelled'),
    ],default='draft',string='Status')
    prescription_lines = fields.One2many('prescription_line.details','prescription_id',string='Prescriptions')
    invoice_ids = fields.Many2many('account.move',string='Invoices')
    picking_ids = fields.One2many("stock.picking",'partner_id', string="Pickings")
    delivery_count = fields.Integer(compute='_compute_delivery_count',string='Delivery Count',store=True)

    @api.depends('picking_ids.partner_id')
    def _compute_delivery_count(self):
        for rec in self:
            rec.delivery_count = len(rec.picking_ids)

    def action_open_delivery(self):
        form_view_id = self.env.ref('stock.view_picking_form').id
        list_view_id = self.env.ref('stock.vpicktree').id

        res = {
            'name': 'Stock Pickings',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'target': 'current',
            'view_id': form_view_id,
            'context': {'default_picking_ids': [self.id]}
        }

        if self.delivery_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('partner_id', '=', self.patient_id.partner_id.id)]

        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Prescription, self).create(vals_list)
        for result in res:
            result.prescription_code = self.env['ir.sequence'].next_by_code('prescription.details')
        return res

    def action_confirm(self):
        self.state = 'confirm'

    def action_cancel(self):
        self.state = 'cancel'

    def action_create_invoice(self):
        if not self.prescription_lines:
            raise ValidationError("Please add prescription lines before creating an invoice.")
        if not self.state == 'confirm':
            raise ValidationError("Prescription must be confirmed before creating an invoice.")
        values = self.action_prepare_invoice_values()
        invoice_id = self.env['account.move'].create(values)
        line_vals_list = self.prepare_invoice_line_vals(invoice_id)
        line_ids = self.env['account.move.line'].create(line_vals_list)
        self.invoice_ids = [(6,0,[invoice_id.id])]

    def action_prepare_invoice_values(self):
        values = {
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.partner_id.id,
            'partner_shipping_id': self.patient_id.partner_id.id,
            'company_id': self.env.user.company_id.id,
            'invoice_line_ids': [],
            'invoice_date':self.date,
            'user_id': self.env.user.id,
        }
        return values

    def prepare_invoice_line_vals(self,invoice_id):
        line_vals_list = []
        for line in self.prescription_lines:
            line_vals = {
                'product_id':line.product_id.id,
                'quantity':line.qty,
                'price_unit':line.price_unit,
                'discount':0.0,
                'move_id':invoice_id.id,
            }
            line_vals_list.append(line_vals)
        return line_vals_list

    def action_create_delivery(self):
        '''
        stock.picking
        stock.move
        '''

        picking_vals = self.prepare_picking_vals()
        picking_id = self.env['stock.picking'].create(picking_vals)
        move_vals = self.prepare_move_vals(picking_id)
        move_ids = self.env['stock.move'].create(move_vals)
        # print("picking_id==========", picking_id)

    def prepare_picking_vals(self):
        picking_type_id = self.env['stock.picking.type'].search([('code','=','outgoing')],limit=1)
        vals = {
            'partner_id': self.patient_id.partner_id.id,
            'picking_type_id':picking_type_id.id,
            'location_id':picking_type_id.default_location_src_id.id,
            'location_dest_id':picking_type_id.default_location_dest_id.id,
            'origin':self.prescription_code,
        }
        return vals

    def prepare_move_vals(self,picking_id):
        move_vals =[]
        for line in self.prescription_lines:
            vals = {
                'picking_type_id':picking_id.picking_type_id.id,
                'location_id':picking_id.location_id.id,
                'location_dest_id':picking_id.location_dest_id.id,
                'picking_id':picking_id.id,
                'product_id':line.product_id.id,
                'name':line.product_id.display_name,
                'product_uom_qty':line.qty,
            }
            move_vals.append(vals)
        return move_vals