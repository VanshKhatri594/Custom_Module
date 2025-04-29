from odoo import fields,models,api


class ResCompany(models.Model):
    _inherit = 'res.company'

    so_double_validation = fields.Selection([
        ('one_step', 'Confirm sales orders in one step'),
        ('two_step', 'Get 2 levels of approvals to confirm a sales order')
    ], string="Levels of Approvals", default='one_step',
        help="Provide a double validation mechanism for sales")

    so_double_validation_amount = fields.Monetary(string='Double validation amount', default=5000,
                                                  help="Minimum amount for which a double validation is required")