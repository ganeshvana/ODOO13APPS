# -*- encoding: utf-8 -*-
{
    "name": "Credit limit based on value and Period - Delivered Quantity(Override)",
    "version": "13.0.1.0.0",
    "summary": "This module is to calculate the credit limit and days limit for the customer based on delivered quantity with override option in delivery order.",
    "license": "OPL-1",
    "depends": ["base", "oi_credit_and_days_limit_delivery_qty", "stock","account" ],
    "author": "Oodu Implementers Private Limited",
    "website": "https://www.odooimplementers.com",
    "category": "Stock & Account",
    "description": "This module is to calculate the credit limit and days limit for the customer based on delivered quantity with override option in delivery order.",
    "data": [
        "security/security.xml",
        "views/picking.xml"
    ],
    "active": False,
    "installable": True,
    
}
