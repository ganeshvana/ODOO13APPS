# -*- coding: utf-8 -*-
{
    'name': 'Product in lead',
    'version': '13.0.1.0.0',
    'category': 'CRM',
    'summary': 'creation of product from lead to quotation',
    'author': 'Oodu Implementers Private Limited',
    'license': 'OPL-1',
    'website': 'https://www.odooimplementers.com',
    'description': 'This module allows to add product in lead and convert to quotation',
    'depends': ['crm','sale_crm','sale','product'],
    'data': [
             'security/ir.model.access.csv',
             'view/lead_view.xml',
             ],
    'images': ['static/description/icon.png'],
    'auto_install': False,
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
