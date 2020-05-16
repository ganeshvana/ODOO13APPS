from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re



class MoveInherit(models.Model):
    _inherit = "account.move"

    def post(self):
        for move in self:
            invoice_total = 0
            payment_total = 0
            exceed_amount = 0
            if self.partner_id.credit_limit_applicable:
                customer_inv = self.env["account.move"].search([('partner_id','=', self.partner_id.id), ('state','not in',['draft','cancel']),('invoice_payment_state','!=','paid'),('type', '=','out_invoice')])
                for inv in customer_inv:
                    invoice_total+= inv.amount_total
                customer_payment = self.env["account.payment"].search([('partner_id','=', self.partner_id.id), ('payment_type', '=','inbound'),('state','in',['posted','reconciled'])])
                for pay in customer_payment:
                    payment_total+= pay.amount
                exceed_amount = (invoice_total + self.amount_total) - payment_total
                if exceed_amount >= self.partner_id.credit_limit:
                    raise UserError(_("Invoice cannot be posted, since the credit limit is exceeded for customer %s") % self.partner_id.name)

            if not move.line_ids.filtered(lambda line: not line.display_type):
                raise UserError(_('You need to add a line before posting.'))
            if move.auto_post and move.date > fields.Date.today():
                date_msg = move.date.strftime(self.env['res.lang']._lang_get(self.env.user.lang).date_format)
                raise UserError(_("This move is configured to be auto-posted on %s" % date_msg))

            if not move.partner_id:
                if move.is_sale_document():
                    raise UserError(_("The field 'Customer' is required, please complete it to validate the Customer Invoice."))
                elif move.is_purchase_document():
                    raise UserError(_("The field 'Vendor' is required, please complete it to validate the Vendor Bill."))

            if move.is_invoice(include_receipts=True) and float_compare(move.amount_total, 0.0, precision_rounding=move.currency_id.rounding) < 0:
                raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead. Use the action menu to transform it into a credit note or refund."))

           
            if not move.invoice_date and move.is_invoice(include_receipts=True):
                move.invoice_date = fields.Date.context_today(self)
                move.with_context(check_move_validity=False)._onchange_invoice_date()

            if move.company_id.tax_lock_date and move.date <= move.company_id.tax_lock_date:
                move.date = move.company_id.tax_lock_date + timedelta(days=1)
                move.with_context(check_move_validity=False)._onchange_currency()

        # Create the analytic lines in batch is faster as it leads to less cache invalidation.
        self.mapped('line_ids').create_analytic_lines()
        for move in self:
            if move.auto_post and move.date > fields.Date.today():
                raise UserError(_("This move is configured to be auto-posted on {}".format(move.date.strftime(self.env['res.lang']._lang_get(self.env.user.lang).date_format))))

            move.message_subscribe([p.id for p in [move.partner_id, move.commercial_partner_id] if p not in move.sudo().message_partner_ids])

            to_write = {'state': 'posted'}

            if move.name == '/':
                sequence = move._get_sequence()
                if not sequence:
                    raise UserError(_('Please define a sequence on your journal.'))

                to_write['name'] = sequence.next_by_id(sequence_date=move.date)

            move.write(to_write)

            # Compute 'ref' for 'out_invoice'.
            if move.type == 'out_invoice' and not move.invoice_payment_ref:
                to_write = {
                    'invoice_payment_ref': move._get_invoice_computed_reference(),
                    'line_ids': []
                }
                for line in move.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable')):
                    to_write['line_ids'].append((1, line.id, {'name': to_write['invoice_payment_ref']}))
                move.write(to_write)

            if move == move.company_id.account_opening_move_id and not move.company_id.account_bank_reconciliation_start:
               
                move.company_id.account_bank_reconciliation_start = move.date

        for move in self:
            if not move.partner_id: continue
            if move.type.startswith('out_'):
                field='customer_rank'
            elif move.type.startswith('in_'):
                field='supplier_rank'
            else:
                continue
            try:
                with self.env.cr.savepoint():
                    self.env.cr.execute("SELECT "+field+" FROM res_partner WHERE ID=%s FOR UPDATE NOWAIT", (move.partner_id.id,))
                    self.env.cr.execute("UPDATE res_partner SET "+field+"="+field+"+1 WHERE ID=%s", (move.partner_id.id,))
                    self.env.cache.remove(move.partner_id, move.partner_id._fields[field])
            except psycopg2.DatabaseError as e:
                if e.pgcode == '55P03':
                    _logger.debug('Another transaction already locked partner rows. Cannot update partner ranks.')
                    continue
                else:
                    raise e