from odoo import fields,models,api


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    so_order_approval = fields.Boolean("Sale Order Approval",
                                       default=lambda self: self.env.company.po_double_validation == 'two_step')
    so_double_validation = fields.Selection(related='company_id.so_double_validation', string="Levels of Approvals *",
                                            readonly=False)
    so_double_validation_amount = fields.Monetary(related='company_id.so_double_validation_amount',
                                                  string="Minimum Amount", currency_field='company_currency_id',
                                                  readonly=False)

    expiry_reminder = fields.Boolean(
        string='Enable Quotation Expiry Reminders',
        config_parameter='sale_approval.expiry_reminder'
    )
    quote_expiry_notify_days = fields.Integer(
        string='Quote Notification Before Expiry (days)',
        default=5,
        config_parameter='sale_approval.quote_expiry_notify_days'
    )


    def set_values(self):
        super().set_values()
        so_double_validation = 'two_step' if self.so_order_approval else 'one_step'
        if self.so_double_validation != so_double_validation:
            self.so_double_validation = so_double_validation