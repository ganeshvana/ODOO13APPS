from odoo import api, fields, models,_


class SaleApprovalSettings(models.Model):
    _name = 'sale.approval.settings'
    _description ='Sale Approval Settings'

    name = fields.Char(string='Purchase Approval Settings')
    approval_currency_id = fields.Many2one('res.currency', string='Currency')
    minimum_total_amount = fields.Float(string='Minimum Total Amount')
    maximum_total_amount = fields.Float(string='Maximum Total Amount')
    level_one_id = fields.Many2one('res.users',string= "Level 1")






