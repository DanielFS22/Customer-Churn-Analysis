-- total de registros 
SELECT COUNT(*) AS total_costumers
FROM customers_churn;

--taxa total de churn geral
SELECT
    churn,
    COUNT(*) AS total,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT (*) customers_churn), 2) AS percentage
    FROM customers_churn
    GROUP BY churn;

--Receita média por status de churn
SELECT
    churn,
    ROUND(AVG(total_revenue), 2) AS avg_revenue
FROM customers_churn
GROUP BY churn;

--Ticket médio por status
SELECT
    churn,
    ROUND(AVG(average_ticket), 2) AS average_ticket
FROM customers_churn
GROUP BY churn;

--Clientes com maior risco (mais de 180 dias sem comprar)
SELECT *
FROM customers_churn
WHERE days_since_last_purchase > 180;
