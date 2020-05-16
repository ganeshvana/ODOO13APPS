from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    credit_limit_checked = fields.Boolean("Credit Limit Checked", default=False)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        invoice_total = 0
        payment_total = 0
        exceed_amount = 0
        due = 0

        if self.partner_id.credit_limit_applicable == True:
            ordered_quantity = all(line.product_id.invoice_policy == 'order' for line in self.order_line)
            if not ordered_quantity:
                raise UserError(_('Select all products with Ordered quantities Invoicing policy'))
            customer_inv = self.env["account.move"].search([('partner_id','=', self.partner_id.id), ('state','not in',['draft','cancel']),('type', '=','out_invoice')])
            for inv in customer_inv:
                invoice_total+= inv.amount_total
                due += inv.amount_residual
                payment_total = invoice_total - due
            
            if payment_total > invoice_total:
                self._action_confirm()
                if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                    self.action_done()
            if invoice_total > payment_total:
                exceed_amount = (invoice_total + self.amount_total) - payment_total
            if ordered_quantity:
                if exceed_amount >= self.partner_id.credit_limit:
                    if self.credit_limit_checked == False:
                        return {
                            "type": "ir.actions.act_window",
                            "res_model": "credit.limit.warning",
                            "views": [[False, "form"]],
                            "target": "new",
                        }
                    elif self.credit_limit_checked == True:
                        self._action_confirm()
                        if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                            self.action_done()
                elif exceed_amount < self.partner_id.credit_limit:
                    self._action_confirm()
                    if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                        self.action_done()
            else:
                raise UserError(_('Select all products with Ordered quantities Invoicing policy'))
        else:
            self._action_confirm()
            if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                self.action_done()
            return True
