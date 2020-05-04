    # -*- encoding: utf-8 -*-
{
    "name": "Customer Credit Limit - Ordered Quantity(Override)",
    "version": "13.0.1.0.0",
    "summary": "This module is to calculate the credit limit for the customer based on ordered quantity with override in invoice.",
    "license": "OPL-1",
    "depends": ["base", "sale", "stock","oi_credit_and_days_limit_order_qty","account"],
    "author": "Oodu Implementers Private Limited",
    "website": "https://www.odooimplementers.com",
    "category": "Account",
    "description": "This module is to calculate the credit limit for the customer based on ordered quantity with override in invoice.",
    "data": [
        "security/security.xml",
        "views/invoice.xml"
    ],
    "active": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
