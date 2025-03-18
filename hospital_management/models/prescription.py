from odoo import fields, models, api


class Prescription(models.Model):
    _name = 'prescription_details'
    _description = 'prescription Information'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    date = fields.Datetime(string='Date', required=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('cancel','Cancelled')
    ])
    prescription_lines = fields.One2many('prescription_line.details','product_id',string='Prescriptions')