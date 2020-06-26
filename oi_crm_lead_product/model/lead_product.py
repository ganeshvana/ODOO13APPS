# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError



######Lead Inherited to add product lines##########

class LeadProduct(models.Model):
    _inherit = 'crm.lead'

    product_ids = fields.One2many('crm.product_line', 'lead_line', string="Product")

####### Function to pass product lines to quotation##########
    def sale_action_quotations_new(self):
        vals = {'partner_id': self.partner_id.id,
                'user_id': self.user_id.id,
                'opportunity_id':self.id

                }
        if self.partner_id:
            sale = self.env['sale.order'].create(vals)
        else:
            raise UserError('Please choose customer for converting to quotation!')

        line = self.env['sale.order.line']
        for data in self.product_ids:
            sale_data = {
                        'order_id': sale.id,
                        'product_id': data.product_id.id,
                        'name': data.name,
                        'product_uom_qty': data.product_uom_qty,
                        'tax_id':[(6, 0, data.tax_ids.ids)],
                        'price_unit': data.price_unit,
                }
            # if self.partner_id:
            #     line.create(sale_data)
            # else:
            #     raise UserError('Please choose customer for converting to quotation!')

        get_data = self.env.ref('sale.view_order_form')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': sale.id,
            'get_data': get_data.id,
        }


########## Product Lines ##########

class productline(models.Model):
    _name = 'crm.product_line'

    product_id = fields.Many2one('product.product', change_default=True, ondelete='restrict', required=True, domain =[('sale_ok', '=', True)])
    name = fields.Text(string='Description')
    product_uom_qty = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit price')
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    lead_line = fields.Many2one('crm.lead')


########## product onchange to get description and sales price #########

    # @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        for record in self:
            name = record.name_get()[0][1]
            record.price_unit = record.product_id.lst_price
            record.tax_ids = record.product_id.taxes_id.ids

            if record.product_id.description_sale:
                name += '\n' + record.product_id.description_sale
                record.name = name

            else:
                record.name = name


    # @api.multi
    def name_get(self):
        result = []
        for lead_line in self:
            name = '%s' % (lead_line.product_id.name)
            if lead_line.product_id:
                name = '[%s] %s' % (lead_line.product_id.default_code, name)
            result.append((lead_line.id, name))
        return result
    

