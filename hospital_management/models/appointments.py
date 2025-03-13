from pkg_resources import require

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Appointments(models.Model):
    _name = 'hospital.appointments'
    _description = 'Appointments'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    appointment_id = fields.Char(string='Appointment ID',readonly=True)
    appointment_date = fields.Date(string='Appointment Date',default=fields.Date.today(),required=True)
    appointment_reason = fields.Text(string='Appointment Reason')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('waiting', 'Waiting'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')],
                             string="Status", default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Appointments, self).create(vals_list)
        for record in res:
            record.appointment_id = self.env['ir.sequence'].next_by_code('hospital.appointments')
        return res

    @api.constrains('appointment_date')
    def check_appointment_date(self):
        for record in self:
            if record.appointment_date < fields.Date.today():
                raise ValidationError('Appointment Date should be greater than or equal to today')
