    # -*- encoding: utf-8 -*-
{
    "name": "Credit limit based on value and period and No of Invoices - Ordered Quantity(Override)",
    "version": "13.0.1.0.0",
    "summary": "This module is to calculate the credit limit,days limit and no.of invoice limit for the customer based on ordered quantity with override option in invoice.",
    "license": "OPL-1",
    "depends": ["base", "sale", "stock","oi_all_limit_order_qty","account"],
    "author": "Oodu Implementers Private Limited",
    "website": "https://www.odooimplementers.com",
    "category": "Partner",
    "description": "This module is to calculate the credit limit, days limit and no.of invoice limit for the customer based on ordered quantity with override option in invoice.",
    "data": [
        "security/security.xml",
        "views/invoice.xml"
    ],
    'images': ['static/description/main_screenshot.png'],

    "active": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
