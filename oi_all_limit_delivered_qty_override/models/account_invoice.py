from odoo import api, fields, models, _
from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils

class Invoice(models.Model):
    _inherit = 'account.move'

  
    today_date = fields.Date(string="Current Date", default=fields.Date.today)

    def action_post(self):
        invoice_total = 0
        cus_sale_amount = 0
        cus_sale = 0

        cus_inv_count = self.env["account.move"].search([('partner_id','=', self.partner_id.id),('state','in',['posted']),('type', '=','out_invoice'),('invoice_payment_state', '!=','paid')])
        cus_inv = self.env["account.move"].search([('partner_id','=', self.partner_id.id),('state','in',['posted']),('type', '=','out_invoice'),('invoice_payment_state', '!=','paid')])
        account_amount = self.amount_total
        print ("SDSSSSSSS",account_amount)
        acc = len(cus_inv)
        # if acc == 0:
        #     cus_sale = account_amount
        #     print ("SSSSSS",account_amount)
        #     print ("Amount",cus_sale)
        #     if self.partner_id.credit_limit and self.partner_id.credit_limit_applicable: 
        #         if cus_sale > self.partner_id.credit_limit:
        #             raise UserError(_('Credit limit exceeded for this customer'))
        # for account_cou in cus_inv:
        #     cus_sale_amount+= account_cou.amount_total + account_amount
        #     print ("SSSinv",account_amount)
        #     print ("Amount",cus_sale_amount)
            # if self.partner_id.credit_limit and self.partner_id.credit_limit_applicable: 
            #     if cus_sale_amount > self.partner_id.credit_limit:
            #         raise UserError(_('Credit limit exceeded for this customer'))
        print ("Invoice ",cus_inv_count)
        for rec in self:
            invoice_count = len(cus_inv_count)
            invoice_count_total = self.partner_id.invoice_credit_limit
            print ("Invoice Count",invoice_count)
            if self.partner_id.invoice_credit_limit_applicable == True:
                print ("Total Invoice", invoice_count)
                print ("Total Invoice Limit",invoice_count)

                if invoice_count >= invoice_count_total:
                    print ("UserError")
                    raise UserError(_('Invoice limit exceeded for this customer'))
        for rec in cus_inv:
        	if self.partner_id.date_credit_limit_applicable == True:
		        print("Total Invoice",rec)
		        today = self.today_date
		        print("Today ",today)
		        invoice = rec.invoice_date
		        print("Invoice ",invoice)
		        dates_cou = self.partner_id.date_credit_limit
		        print("Dates_cou ",dates_cou)
		        deltaas = today - invoice
		        print("Total Days",deltaas.days)
		        invoice_expiry = (deltaas).days
		        print("Expiry",invoice_expiry)

		        if invoice_expiry >= self.partner_id.date_credit_limit:
		        	print ("UserError")
		        	raise UserError(_('Days limit exceeded for this customer'))


        if self.mapped('line_ids.payment_id') and any(post_at == 'bank_rec' for post_at in self.mapped('journal_id.post_at')):
            raise UserError(_("A payment journal entry generated in a journal configured to post entries only when payments are reconciled with a bank statement cannot be manually posted. Those will be posted automatically after performing the bank reconciliation."))
        return self.post()
         