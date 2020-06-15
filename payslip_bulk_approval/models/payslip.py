from odoo import api, fields, models, _


class HrPayslipInherit(models.Model):
	_inherit = 'hr.payslip'


	def action_approve(self):
		self.write({'state': 'done'})
		return True
