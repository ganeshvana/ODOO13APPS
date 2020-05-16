# -*- encoding: utf-8 -*-
{
    "name": "Credit limit based on value and Period - Ordered Quantity",
    "version": "13.0.1.0.0",
    "summary": "This module is to calculate the credit limit and days limit for the customer based on ordered quantity.",
    "license": "OPL-1",
    "depends": ["base", "sale", "stock","account"],
    "author": "Oodu Implementers Private Limited",
    "website": "https://www.odooimplementers.com",
    "category": "Partner",
    "description": "This module is to calculate the credit limit and days limit for the customer based on ordered quantity.",
    "data": [
        "wizard/credit_limit_warning.xml",
        "views/partner.xml",
        "security/security.xml",
        "security/ir.model.access.csv"
    ],
    "active": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
