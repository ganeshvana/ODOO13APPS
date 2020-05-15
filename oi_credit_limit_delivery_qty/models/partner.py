from odoo import api, fields, models, _

class res_partner(models.Model):
    _inherit = "res.partner"

    credit_limit = fields.Integer(string="Credit Limit")
    credit_limit_applicable = fields.Boolean("Credit Limit Applicable")
  


