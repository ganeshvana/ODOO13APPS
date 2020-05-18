# -*- coding: utf-8 -*-
{
    "name": "Credit limit based on value and period and No of Invoices - Delivered Quantity",
    "version": "13.0.1.0.0",
    "summary": "This module is to calculate the credit limit, days and invoice limit for the customer based on delivered quantity.",
    "license": "OPL-1",
    "depends": ["base", "sale", "stock", ],
    "author": "Oodu Implementers Private Limited",
    "website": "https://www.odooimplementers.com",
    "category": "Partner",
    "description": "This module is to calculate the credit limit, days limit and invoice limit for the customer based on delivered quantity.",
    "data": [
        "wizard/credit_limit_warning.xml",
        "views/partner.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
    ],
    "images": ['static/description/icon.png'],
    'auto_install': False,
    'installable': True,
    'application': False,
}