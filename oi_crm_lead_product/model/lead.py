# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Lead(models.Model):
    _inherit = 'crm.lead'

    product_line_id = fields.One2many('crm.product_line',inverse_name='lead_line')
