from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError


class PurchaseApprovalSettings(models.Model):
    _name = 'purchase.approval.settings'
    _description ='Purchase Approval Settings'
    _rec_name = 'code'

    code = fields.Char(string="Code",readonly=True, required=True, copy=False, default='New')
    approval_currency_id = fields.Many2one('res.currency', string='Currency',required=True)
    minimum_total_amount = fields.Float(string='Minimum Total Amount',required=True, default=1.00)
    maximum_total_amount = fields.Float(string='Maximum Total Amount',required=True)
    level_one_id = fields.Many2one('res.users',string= "Level 1")
    level_two_id = fields.Many2one('res.users',string= "Level 2")

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('purchase.approval.settings') or 'New'
        result = super(PurchaseApprovalSettings, self).create(vals)
        return result


    @api.constrains('maximum_total_amount','minimum_total_amount')
    def maximum(self):
        if self.minimum_total_amount >= self.maximum_total_amount:
            raise UserError(_("You Have To Enter The Maximum Total Amount above The Minimum Total Amount"))
        if self.minimum_total_amount < 1.00:
            raise UserError(_("You have to enter at least 1 Rs For Minimum Total Amount"))


    @api.constrains('level_one_id','level_two_id')
    def level(self):
        if not self.level_two_id and not self.level_one_id:
            raise UserError(_("Please Select Levels"))








