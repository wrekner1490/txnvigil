-- ============================================================================
-- TxnVigil - SQL fraud analytics (SQLite; same SQL works in PostgreSQL)
-- Load:  python src/load_sql.py   ->  data/txnvigil.db, table `txn`
-- Run:   sqlite3 data/txnvigil.db < sql/fraud_queries.sql
-- ============================================================================

-- Q1. Overall fraud rate and fraud value by channel (GROUP BY + conditional aggregation)
SELECT channel,
       COUNT(*)                                        AS txns,
       SUM(is_fraud)                                   AS fraud_txns,
       ROUND(100.0 * SUM(is_fraud) / COUNT(*), 3)      AS fraud_rate_pct,
       ROUND(SUM(CASE WHEN is_fraud = 1 THEN amount END), 0) AS fraud_value
FROM txn
GROUP BY channel;

-- Q2. Velocity: customers with 3+ txns inside any 60-minute window (self-join on time range)
SELECT a.user_id, a.txn_id, a.ts, COUNT(*) AS txns_last_60m
FROM txn a
JOIN txn b
  ON b.user_id = a.user_id
 AND b.ts_epoch BETWEEN a.ts_epoch - 3600 AND a.ts_epoch
GROUP BY a.user_id, a.txn_id
HAVING COUNT(*) >= 3
ORDER BY txns_last_60m DESC
LIMIT 20;

-- Q3. Amount vs customer's own history (window function: running average of PAST txns only)
WITH hist AS (
  SELECT txn_id, user_id, ts, amount, is_fraud,
         AVG(amount) OVER (PARTITION BY user_id ORDER BY ts
                           ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS past_avg
  FROM txn
)
SELECT txn_id, user_id, ts, amount, ROUND(past_avg, 0) AS past_avg,
       ROUND(amount / past_avg, 1) AS x_times_usual, is_fraud
FROM hist
WHERE past_avg IS NOT NULL AND amount > 10 * past_avg
ORDER BY x_times_usual DESC
LIMIT 20;

-- Q4. Mule detection: payees receiving from many DISTINCT first-time senders in a day
WITH first_pay AS (
  SELECT payee_id, user_id, MIN(ts) AS first_ts
  FROM txn GROUP BY payee_id, user_id
)
SELECT payee_id, DATE(first_ts) AS day, COUNT(*) AS new_senders
FROM first_pay
GROUP BY payee_id, DATE(first_ts)
HAVING COUNT(*) >= 8
ORDER BY new_senders DESC
LIMIT 20;

-- Q5. Time between consecutive txns of a customer (LAG) - rapid-fire draining
SELECT txn_id, user_id, ts, amount, is_fraud,
       ts_epoch - LAG(ts_epoch) OVER (PARTITION BY user_id ORDER BY ts) AS secs_since_prev
FROM txn
ORDER BY user_id, ts
LIMIT 50;

-- Q6. Micro-transaction testing: Rs.1-10 txns followed by a large one to the same payee
WITH seq AS (
  SELECT txn_id, user_id, payee_id, ts, amount, is_fraud,
         LAG(amount, 1) OVER w AS prev1,
         LAG(amount, 2) OVER w AS prev2
  FROM txn
  WINDOW w AS (PARTITION BY user_id, payee_id ORDER BY ts)
)
SELECT * FROM seq
WHERE prev1 <= 10 AND prev2 <= 10 AND amount > 1000
LIMIT 20;

-- Q7. Rank customers by fraud loss (RANK) and top-3 riskiest hours
SELECT user_id, ROUND(SUM(amount), 0) AS fraud_loss,
       RANK() OVER (ORDER BY SUM(amount) DESC) AS loss_rank
FROM txn WHERE is_fraud = 1
GROUP BY user_id
ORDER BY loss_rank LIMIT 10;

SELECT CAST(strftime('%H', ts) AS INT) AS hour,
       ROUND(100.0 * SUM(is_fraud) / COUNT(*), 3) AS fraud_rate_pct
FROM txn GROUP BY hour ORDER BY fraud_rate_pct DESC LIMIT 3;
