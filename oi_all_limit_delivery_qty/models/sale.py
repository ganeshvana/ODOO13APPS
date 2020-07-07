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
        sale_total = 0
        overall_sale_total = 0
        due = 0

        if self.partner_id.credit_limit_applicable ==True and self.partner_id.credit_limit > 0:
            print ("ttttttttt")
            delivered_quantity = all(line.product_id.invoice_policy == 'delivery' for line in self.order_line)
            customer_inv = self.env["account.move"].search([('partner_id','=', self.partner_id.id), ('state','not in',['draft','cancel']),('type', '=','out_invoice')])
            for inv in customer_inv:
                invoice_total+= inv.amount_total
                due += inv.amount_residual
            # customer_payment = self.env["account.payment"].search([('partner_id','=', self.partner_id.id), ('payment_type', '=','inbound'),('state','in',['posted','reconciled'])])
            # for pay in customer_payment:
            #     payment_total+= pay.amount
                payment_total = invoice_total - due
                print ("invvv",invoice_total,payment_total)

            sale = self.env['sale.order'].search([('partner_id','=', self.partner_id.id),('state','not in',['draft','cancel'])])
            for total in sale:
                sale_total+= total.amount_total
                overall_sale_total = sale_total - payment_total
                print ("Sale total", overall_sale_total,sale_total,self.partner_id.credit_limit)
                if self.partner_id.credit_limit > 0 and self.partner_id.credit_limit_applicable:
                    print ("SSS")
                    if overall_sale_total > self.partner_id.credit_limit:
                        if self.credit_limit_checked == False:
                            return {
                                "type": "ir.actions.act_window",
                                "res_model": "credit.limit.warning",
                                "views": [[False, "form"]],
                                "target": "new",
                            }
            if payment_total > invoice_total:
                print ("else")
            if invoice_total > payment_total:
                exceed_amount = (invoice_total + self.amount_total) - payment_total
            if not delivered_quantity:
                print ("ppppp")
                raise UserError(_('Please select delivered quantities as invoicing policy'))
            if delivered_quantity:
                print ("gggggg")
                if exceed_amount > self.partner_id.credit_limit:
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
                raise UserError(_('Select all products with Delivered quantities Invoicing policy'))
        else:
            print ("rrrrrrrr")
            self._action_confirm()
            if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                self.action_done()
            return True
