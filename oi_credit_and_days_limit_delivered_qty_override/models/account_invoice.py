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
        
        cus_inv = self.env["account.move"].search([('partner_id','=', self.partner_id.id),('state','in',['posted']),('type', '=','out_invoice'),('invoice_payment_state', '!=','paid')])
        
       
        for rec in cus_inv:
        	if self.partner_id.date_credit_limit_applicable == True:
		        today = self.today_date
		        invoice = rec.invoice_date
		        dates_cou = self.partner_id.date_credit_limit
		        deltaas = today - invoice
		        invoice_expiry = (deltaas).days

		        if invoice_expiry >= self.partner_id.date_credit_limit:
		        	raise UserError(_('Days limit exceeded for this customer'))


        if self.mapped('line_ids.payment_id') and any(post_at == 'bank_rec' for post_at in self.mapped('journal_id.post_at')):
            raise UserError(_("A payment journal entry generated in a journal configured to post entries only when payments are reconciled with a bank statement cannot be manually posted. Those will be posted automatically after performing the bank reconciliation."))
        return self.post()
         