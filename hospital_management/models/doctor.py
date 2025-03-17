from odoo import models, fields, api


class Doctor(models.Model):
    _name = 'res.doctor'
    _description = 'Doctor Information'
    # _inherit = 'res.partner'

    name = fields.Char(string='Doctor Name')
    specialization = fields.Many2one('hospital.specialization', string='Specialization')
    license_no = fields.Char(string='License Number',unique=True)
    experience_years = fields.Integer(string='Experience in Years')
    hospital_id = fields.Many2one('hospital.hospital', string='Associated Hospital/Clinic')
    is_emergency_available = fields.Boolean(string='Emergency Availability')
