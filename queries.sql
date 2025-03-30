-- 1. Count finance lending and blockchain clients
SELECT COUNT(*) AS finance_blockchain_clients
FROM clients
WHERE industry IN ('Finance Lending', 'Blockchain');

-- 2. Find the industry with the highest renewal rate
SELECT industry, COUNT(*) AS renewal_count
FROM clients c
JOIN subscriptions s ON c.id = s.client_id
WHERE s.renewal_date IS NOT NULL
GROUP BY industry
ORDER BY renewal_count DESC
LIMIT 1;

-- 3. Calculate the average inflation rate at the time of renewal
SELECT AVG(ir.inflation_rate) AS avg_inflation_at_renewal
FROM subscriptions s
JOIN inflation_rates ir ON DATE(s.renewal_date) = DATE(ir.date);

-- 4. Find the median amount paid per year for all payment methods
WITH PaymentAmounts AS (
    SELECT amount_paid, 
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount_paid) OVER () AS median_amount
    FROM subscriptions
)
SELECT DISTINCT median_amount FROM PaymentAmounts;