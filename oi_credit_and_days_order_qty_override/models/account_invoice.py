from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Invoice(models.Model):
    _inherit = 'account.move'

    override_credit_limit = fields.Boolean("Override Credit Limit")
    today_date = fields.Date(string="Current Date", default=fields.Date.today)

    def action_post(self):
        if self.type == 'out_invoice':
            invoice_total = 0
            payment_total = 0
            exceed_amount = 0
            due = 0
            customer_inv = self.env["account.move"].search([('partner_id','=', self.partner_id.id), ('state','not in',['draft','cancel']),('type', '=','out_invoice')])
            print ("customer_inv",customer_inv)
            for inv in customer_inv:
                invoice_total+= inv.amount_total
                due += inv.amount_residual
                print ('invoice_total',invoice_total, due, inv.invoice_payment_state)
            

                payment_total = invoice_total - due
                print ('payment_total',payment_total)
            cus_inv = self.env["account.move"].search([('partner_id','=', self.partner_id.id),('state','in',['posted']),('type', '=','out_invoice'),('invoice_payment_state', '!=','paid')])
            cus_inv_count = self.env["account.move"].search([('partner_id','=', self.partner_id.id),('state','in',['posted']),('type', '=','out_invoice'),('invoice_payment_state', '!=','paid')])
            sale = self.env['sale.order'].search([('name','=',self.invoice_origin)])
            ordered_quantity = all(line.product_id.invoice_policy == 'order' for line in self.invoice_line_ids)

            cus_invoice = self.amount_total
            if not self.override_credit_limit:
                if cus_invoice >= self.partner_id.credit_limit:
                    raise UserError(_('Credit limit exceeded for this customer'))

            for rec in cus_inv:
                if self.partner_id.date_credit_limit > 0:
                    today = self.today_date
                    invoice = rec.invoice_date
                    dates_cou = self.partner_id.date_credit_limit
                    deltaas = today - invoice
                    invoice_expiry = (deltaas).days

                    if invoice_expiry >= self.partner_id.date_credit_limit:
                        raise UserError(_('Days limit exceeded for this customer'))

            if payment_total > invoice_total:
                print ("else")
                if self.mapped('line_ids.payment_id') and any(post_at == 'bank_rec' for post_at in self.mapped('journal_id.post_at')):
                    raise UserError(_("A payment journal entry generated in a journal configured to post entries only when payments are reconciled with a bank statement cannot be manually posted. Those will be posted automatically after performing the bank reconciliation."))
                return self.post()
            if payment_total < invoice_total:
                print ("invoice_payment",invoice_total,payment_total)
                # exceed_amount = (invoice_total + sale.amount_total) - payment_total
                exceed_amount = (invoice_total + self.amount_total) - payment_total
                print ("escee",exceed_amount)
                if self.partner_id.credit_limit_applicable and not self.override_credit_limit:
                    if exceed_amount > self.partner_id.credit_limit :
                            raise UserError(_('Credit limit exceeded for this customer'))

            if ordered_quantity:
                if self.partner_id.credit_limit and self.partner_id.credit_limit_applicable:
                    print ("ordered_quantity",exceed_amount)
                    if exceed_amount > self.partner_id.credit_limit:
                        
                        if self.override_credit_limit:
                            if self.mapped('line_ids.payment_id') and any(post_at == 'bank_rec' for post_at in self.mapped('journal_id.post_at')):
                                raise UserError(_("A payment journal entry generated in a journal configured to post entries only when payments are reconciled with a bank statement cannot be manually posted. Those will be posted automatically after performing the bank reconciliation."))
                            return self.post()
                        else:
                            
                            raise UserError(_('Credit limit exceeded for this customer'))
                    else:
                        if self.mapped('line_ids.payment_id') and any(post_at == 'bank_rec' for post_at in self.mapped('journal_id.post_at')):
                            raise UserError(_("A payment journal entry generated in a journal configured to post entries only when payments are reconciled with a bank statement cannot be manually posted. Those will be posted automatically after performing the bank reconciliation."))
                        return self.post()
                else:
                        if self.mapped('line_ids.payment_id') and any(post_at == 'bank_rec' for post_at in self.mapped('journal_id.post_at')):
                            raise UserError(_("A payment journal entry generated in a journal configured to post entries only when payments are reconciled with a bank statement cannot be manually posted. Those will be posted automatically after performing the bank reconciliation."))
                        return self.post()
            else:
                raise UserError(_('Select all products with Ordered quantities Invoicing policy'))
        else:
            # if self.mapped('line_ids.payment_id') and any(post_at == 'bank_rec' for post_at in self.mapped('journal_id.post_at')):
            #     raise UserError(_("A payment journal entry generated in a journal configured to post entries only when payments are reconciled with a bank statement cannot be manually posted. Those will be posted automatically after performing the bank reconciliation."))
            return self.post()
