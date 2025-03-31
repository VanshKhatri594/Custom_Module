from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Prescription(models.Model):
    _name = 'prescription_details'
    _description = 'prescription Information'
    _rec_name = 'patient_id'


    patient_id = fields.Many2one('hospital.patient', string='Patient')
    date = fields.Datetime(string='Date', required=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('cancel','Cancelled'),
    ],default='draft',string='Status')
    prescription_lines = fields.One2many('prescription_line.details','prescription_id',string='Prescriptions')
    invoice_ids = fields.Many2many('account.move',string='Invoices')

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