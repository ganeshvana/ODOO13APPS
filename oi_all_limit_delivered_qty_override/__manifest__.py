# -*- encoding: utf-8 -*-
{
    "name": "Credit limit based on value and period and No of Invoices - Delivered Quantity(Override)",
    "version": "13.0.1.0.0",
    "summary": "This module is to calculate the credit limit for the customer based on delivered quantity with override in delivery order.",
    "license": "OPL-1",
    "depends": ["base","stock","oi_all_limit_delivery_qty"],
    "author": "Oodu Implementers Private Limited",
    "website": "https://www.odooimplementers.com",
    "category": "Account & Stock",
    "description": "This module is to calculate the credit limit for the customer based on delivered quantity with override in delivery order.",
    "data": [
        "security/security.xml",
        "views/picking.xml"
    ],
    "images": ['static/description/banner.gif'],
    "active": False,
    "installable": True,
}
