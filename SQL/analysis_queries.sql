USE churn_project;

-- Quantos clientes existem na base?
SELECT COUNT(*) AS total_clientes
FROM customers_churn;

-- Qual o percentual de clientes que cancelaram?
SELECT 
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 
        / COUNT(*), 
    2) AS taxa_churn_percentual
FROM customers_churn;

-- Clientes que cancelam geram mais ou menos receita?
SELECT
	churn,
    ROUND(AVG(total_revenue), 2) AS receita_media
FROM customers_churn
GROUP BY churn;

-- Ticket médio por status de churn
SELECT
	churn, 
    ROUND(AVG(average_ticket), 2) AS ticket_medio
FROM customers_churn
GROUP BY churn;

-- Receita total perdida com churn
SELECT
	ROUND(SUM(total_revenue),2) AS receita_perdida_total
FROM customers_churn
WHERE churn = 'Yes';

-- Tempo médio sem compra antes do churn
SELECT 
    ROUND(AVG(days_since_last_purchase), 2) AS media_dias_sem_compra
FROM customers_churn
WHERE churn = 'Yes';


--1️⃣ Total de clientes / R: 96096
--2️⃣ Taxa de churn (%) /0.00%
--3️⃣ Receita média churn = ? 
--4️⃣ Receita média não churn = ?
--5️⃣ Ticket médio churn = ?
--6️⃣ Média de dias sem compra antes do churn = ?
--7️⃣ Receita total perdida = ?