# -*- encoding: utf-8 -*-
{
    "name": "Credit limit based on value - Delivered Quantity",
    "version": "13.0.1.0.0",
    "summary": "This module is to calculate the credit limit for the customer based on delivered quantity.",
    "license": "OPL-1",
    "depends": ["base", "sale", "stock", ],
    "author": "Oodu Implementers Private Limited",
    "website": "https://www.odooimplementers.com",
    "category": "Sale & Stock",
    "description": "This module is to calculate the credit limit for the customer based on delivered quantity.",
    "data": [
        "wizard/credit_limit_warning.xml",
        "views/partner.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
    ],
    'images': ['static/description/main_screenshot.png'],
    "active": False,
    "installable": True,
}
