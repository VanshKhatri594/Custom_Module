from os import write

from odoo import fields,models,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError,UserError


class Student(models.Model):
    _name = 'res.student'
    _description = 'Student Information'

    registration_id = fields.Char(string='Registration Id',readonly=True,default='New')
    registration_date = fields.Date(string='Registration Date',required=True)
    name = fields.Char(string='Name',required=True)
    birth_date = fields.Date(string='Birth Date',required=True)
    age = fields.Char(string='Age',compute='_on_compute_age',store=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    is_child = fields.Boolean(default=False)
    standard = fields.Selection([
        ('one','1'),
        ('two','2'),
        ('three', '3'),
        ('four', '4'),
        ('five', '5'),
        ('six', '6'),
        ('seven', '7'),
        ('eight', '8'),
        ('nine', '9'),
        ('ten', '10'),
        ('eleven', '11'),
        ('twelve', '12')
    ])
    guardian_name = fields.Char(string='Guardian Name')
    guardian_phone = fields.Char(string='Guardian Phone')
    fees_id = fields.Many2one('tuition.fees.structure','Tuition Fees')
    fees = fields.Float(string='Fees')
    is_blocked = fields.Boolean(string='Is Blocked')
    is_expired = fields.Boolean(string='Is Expired')
    mark_ids = fields.One2many('previous.year.mark','student_id','Marks')
    state = fields.Selection([
        ('block', 'Blocked'),
        ('unblock', 'Unblocked'),
    ],
        string="Status", default='unblock')

    @api.model_create_multi
    def create(self,vals_list):
        res = super(Student,self).create(vals_list)
        for rec in res:
            rec.registration_id = self.env['ir.sequence'].next_by_code('res.student')
        return res

    @api.depends('birth_date')
    def _on_compute_age(self):
        for record in self:
            record.is_child = False
            if record.birth_date:
                diff = relativedelta(fields.Date.today(), record.birth_date)
                if diff.years < 10:
                    record.is_child = True
                age_res = f"{diff.years} years {diff.months} months"
                record.age = age_res

    @api.constrains('phone')
    def check_phone(self):
        for record in self:
            if record.phone and not record.phone.isdigit():
                raise ValidationError("Phone number should be in digits")

            if record.phone and len(record.phone) < 10:
                raise ValidationError("Phone number should be 10 digits")

            if record.phone:
                dup = self.env['res.student'].search_count([('phone', '=', record.phone)])
                if dup > 1:
                    raise UserError("Phone number already exists")

    def action_block(self):
        for rec in self:
            rec.state = 'block'
            rec.is_blocked = True

    def action_unblock(self):
        for rec in self:
            rec.is_blocked = False
            rec.state = 'unblock'

    def _Registration_Expired(self):
        today = fields.Date.today()
        diff = today - relativedelta(days=30)
        expiry = self.env['res.student'].search([('is_blocked','=',False),('registration_date','<',diff)])
        expiry.write({'is_expired':True})

    def write(self,vals):
        for record in self:
            if record.is_blocked and 'is_blocked' not in vals:
                raise UserError('Blocked Student Cannot edit the details! Please Unblock First')
        res = super().write(vals)
        return res




