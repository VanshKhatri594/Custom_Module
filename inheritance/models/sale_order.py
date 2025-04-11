from odoo import api,models,fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self,vals_list):
       for rec in vals_list:
            partner_id = rec.get('partner_id')
            if partner_id:
                tc = self.env['res.partner'].browse(partner_id)
                if tc.use_customers_tc and tc.terms_and_conditions:
                    rec['note'] = tc.terms_and_conditions
       return super(SaleOrder,self).create(vals_list)

    @api.onchange('partner_id')
    def _on_change_partner(self):
        if self.partner_id:
            self.note = self.partner_id.terms_and_conditions
        else:
            self.note = False


