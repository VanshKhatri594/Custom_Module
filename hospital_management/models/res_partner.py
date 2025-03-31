from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def write(self, vals):
        if self.env.context.get('prevent_recursion'):
            return super(ResPartner, self).write(vals)

        else:
            for rec in self:
                patient = self.env['hospital.patient'].search([('partner_id', '=', rec.id)])
                if patient and ('phone' in vals or 'email' in vals):
                    patient.with_context(prevent_recursion=True).write({
                        'phone': vals.get('phone', rec.phone),
                        'email': vals.get('email', rec.email)
                    })
        return super(ResPartner, self).write(vals)



