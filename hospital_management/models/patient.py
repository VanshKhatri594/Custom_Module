from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date

class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'

    patient_code = fields.Char(string='Patient Id', readonly=True)
    name = fields.Char(string='Name', required=True)
    age = fields.Char(string='Age', readonly=True)
    age_category = fields.Selection([('senior citizen','Senior Citizen'),
                                     ('adult','Adult'), ('child','Child'), ('minor','Minor')],
                                    string='Age Category')
    blood_group = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-')
    ], string='Blood Group', required=True)
    dob = fields.Date(string='Date of Birth', required=True)
    previous_illness = fields.Text(string='Previous Illness')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    guardian_type = fields.Selection([('parent','Parent'),('relative','Relative'),
                                      ('sibling','Sibling'),('friend','Friend'),('other','Other')],string='Guardian Type')
    guardian_id = fields.Many2one('res.partner',String='Guardian')
    appointment_ids = fields.One2many('hospital.appointments', 'patient_id', string="Appointments")

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Patient, self).create(vals_list)
        for record in res:
            record.patient_code = self.env['ir.sequence'].next_by_code('hospital.patient')
        return res

    def action_open_appointments(self):
        view_id = self.env.ref('hospital_management.appointment_form_view').id

        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointments',
            'view_id': view_id,
            'target': 'current',
            'context': {'default_patient_id': self.id}
        }

    @api.constrains('dob')
    def action_calculate_age(self):
        for record in self:
            if record.dob > fields.Date.today():
                raise ValidationError('Date of Birth should be less than or equal to today')
            else:
                today = date.today()
                diff = relativedelta(today,record.dob)
                self.age = f"{diff.years} years {diff.months} months"

    @api.onchange('dob')
    def on_change_dob(self):
        if self.dob:
            today = date.today()
            diff = relativedelta(today,self.dob)
            if diff.years >= 60:
                self.age_category = 'senior citizen'
            elif diff.years >= 18:
                self.age_category = 'adult'
            elif diff.years >= 10:
                self.age_category = 'minor'
            else :
                self.age_category = 'child'

    def _patients_count(self):
        count = self.search_count([('age', '>', 40)])
        print("Total number of patients above 40 years: ", count)




