from odoo import fields,models,api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super(PurchaseOrder,self).button_confirm()
        if self.partner_id and self.partner_id.email:
            template_id = self.env.ref('practical_vansh.email_template_purchase')
            template_id.send_mail(self.id, force_send=True)
        return res