from odoo import api, fields, models,_


class PurchaseApprovalSettings(models.Model):
    _name = 'purchase.approval.settings'
    _description ='Purchase Approval Settings'

    name = fields.Char(string='Purchase Approval Settings')
    approval_currency_id = fields.Many2one('res.currency', string='Currency')
    minimum_total_amount = fields.Float(string='Minimum Total Amount')
    maximum_total_amount = fields.Float(string='Maximum Total Amount')
    level_one_id = fields.Many2one('res.users',string= "Level 1")
    level_two_id = fields.Many2one('res.users',string= "Level 2")






