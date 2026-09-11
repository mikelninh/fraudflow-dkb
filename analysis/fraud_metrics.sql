-- FraudFlow Data & Technology proof
-- Synthetic schema only. These queries are illustrative and are not production bank queries.

-- 1) Data quality pass rate
SELECT
  COUNT(*) AS transactions,
  SUM(CASE WHEN data_complete = 1 THEN 1 ELSE 0 END) AS complete_rows,
  ROUND(100.0 * SUM(CASE WHEN data_complete = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS data_quality_pass_rate
FROM transactions;

-- 2) Alert volume and rate
SELECT
  COUNT(*) AS alert_count,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM transactions), 1) AS alert_rate
FROM transactions
WHERE alert_reason NOT IN ('none', 'data_quality');

-- 3) Analyst outcomes for alerted transactions
SELECT
  analyst_outcome,
  COUNT(*) AS cases
FROM transactions
WHERE alert_reason NOT IN ('none', 'data_quality')
GROUP BY analyst_outcome
ORDER BY cases DESC;

-- 4) Countries with the highest alert share
SELECT
  country,
  COUNT(*) AS transactions,
  SUM(CASE WHEN alert_reason NOT IN ('none', 'data_quality') THEN 1 ELSE 0 END) AS alerts,
  ROUND(
    100.0 * SUM(CASE WHEN alert_reason NOT IN ('none', 'data_quality') THEN 1 ELSE 0 END) / COUNT(*),
    1
  ) AS alert_rate
FROM transactions
GROUP BY country
ORDER BY alert_rate DESC, transactions DESC;
