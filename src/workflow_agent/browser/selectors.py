"""CSS selectors and data-testid helpers."""

SELECTORS = {
    "customers": {
        "page": "/customers",
        "customer_name_input": "[data-testid='customer-name-input']",
        "contact_input": "[data-testid='contact-input']",
        "email_input": "[data-testid='email-input']",
        "region_select": "[data-testid='region-select']",
        "create_btn": "[data-testid='create-customer-btn']",
        "success_message": "[data-testid='success-message']",
        "customer_list": "[data-testid='customer-list']",
        "customer_row": "[data-testid='customer-row']",
        "customer_name": "[data-testid='customer-name']",
        "customer_contact": "[data-testid='customer-contact']",
        "customer_region": "[data-testid='customer-region']",
    },
    "orders": {
        "page": "/orders",
        "order_id_input": "[data-testid='order-id-input']",
        "search_btn": "[data-testid='search-order-btn']",
        "order_result": "[data-testid='order-result']",
        "order_not_found": "[data-testid='order-not-found']",
        "order_result_id": "[data-testid='order-result-id']",
        "order_result_status": "[data-testid='order-result-status']",
        "order_result_amount": "[data-testid='order-result-amount']",
        "order_result_supplier": "[data-testid='order-result-supplier']",
    },
    "reports": {
        "page": "/reports",
        "report_type_select": "[data-testid='report-type-select']",
        "month_input": "[data-testid='month-input']",
        "export_btn": "[data-testid='export-report-btn']",
    },
    "supplier_onboarding": {
        "page": "/supplier-onboarding",
        "company_name_input": "[data-testid='company-name-input']",
        "tax_id_input": "[data-testid='tax-id-input']",
        "region_select": "[data-testid='region-select']",
        "submit_btn": "[data-testid='submit-onboarding-btn']",
    },
}
