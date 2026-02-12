CREATE TABLE customers_churn (
    customer_id VARCHAR(50),
    total_orders INT,
    total_revenue DECIMAL(10,2),
    last_purchase DATETIME,
    days_since_last_purchase INT,
    average_ticket DECIMAL(10,2),
    churn BOOLEAN
);
