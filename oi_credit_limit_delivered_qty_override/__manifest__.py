# -*- encoding: utf-8 -*-
{
    "name": "Credit limit based on value - Delivered Quantity(Override)",
    "version": "13.0.1.0.0",
    "summary": "This module is to calculate the credit limit for the customer based on delivered quantity with override optionin delivery order.",
    "license": "OPL-1",
    "depends": ["base", "oi_credit_limit_delivery_qty", "stock","account" ],
    "author": "Oodu Implementers Private Limited",
    "website": "https://www.odooimplementers.com",
    "category": "Account & Stock",
    "description": "This module is to calculate the credit limit for the customer based on delivered quantity with override option in delivery order.",
    "data": [
        "security/security.xml",
        "views/picking.xml"
    ],
    "active": False,
    "installable": True,
   
}
