# TxnVigil — Interview Prep (IndusInd Management Associate, Fraud Risk)

## 1. The 2-minute pitch

"Banks first catch fraud with rules, but rules are noisy and miss new patterns. I built TxnVigil to measure
how much ML adds on top. I simulated 1.1 million UPI transactions with four real fraud patterns (account takeover,
mule accounts, credential testing, and social-engineering scams). I built behavioural features using only each
transaction's past, and trained gradient-boosted trees on the earlier weeks. On the later, unseen weeks, at the
same analyst workload, the model caught 91% of fraud vs 66% for rules, with 57% fewer alerts. Every alert carries
reason codes for the analyst. The hardest case was APP scams, where the customer authorises the payment
themselves, and that's where combining rules with the model helped most."

## 2. Key concepts you must be able to explain

| Concept | What to say |
|---|---|
| **Class imbalance** | Fraud is 0.33% of txns. A model that says "never fraud" is 99.67% accurate, so accuracy is useless. Use precision, recall and PR-AUC. |
| **Precision vs recall** | Recall = % of fraud caught (lost money). Precision = % of alerts that are real fraud (analyst time and customer friction). Raising one usually lowers the other. |
| **PR-AUC vs ROC-AUC** | ROC-AUC looks great on imbalanced data (mine is 0.999) because there are so many true negatives. PR-AUC (0.947) is the honest metric for rare fraud. |
| **Threshold / alert budget** | The model gives a score; the bank decides the cut-off. I set it so 0.5% of txns are alerted (the capacity an analyst team can review), not the default 0.5. |
| **Time-based split** | Trained on days 0–39, tuned on 40–47, tested on 48–59. A random split leaks future behaviour (the same mule appears in train and test) and inflates scores. |
| **Data leakage** | Every feature uses only the past, e.g. the "customer's average" excludes the current txn and anything after it. |
| **Class weighting vs SMOTE** | I weight fraud rows higher instead of creating synthetic fraud rows. It's simpler and doesn't invent data. Know that SMOTE exists and why some avoid it. |
| **Gradient boosting** | Builds many small decision trees one after another; each corrects the previous ones' errors. XGBoost and LightGBM are faster implementations of the same idea. |
| **Why trees beat logistic regression** | APP scams = new payee AND huge amount AND payee with no history: an *interaction*. Linear models add signals independently; trees split on combinations. LR caught 1% of APP scams; GBT caught 55%. |
| **Rules vs ML vs hybrid** | Rules are explainable and fast to deploy for a newly seen pattern; ML generalises. Banks run both. My hybrid had 95.6% recall but 3× the alerts, which is the trade-off. |
| **Explainability** | Regulators and analysts need to know *why*. I use permutation importance (global) and reason codes per alert. SHAP gives exact per-feature contributions (my next step). |
| **Mule accounts** | Accounts that receive and pass on stolen money. Signals: new or low-history account, many first-time senders in a short window, quick outflow. My top features were payee-side. |
| **Label delay & drift** | Real fraud labels arrive weeks later (complaints, chargebacks). Fraudsters adapt, so models need monitoring and retraining. |
| **Simulated data limitation** | Say it before they do: "The data is simulated, so real numbers would be lower. What carries over is the method: leakage-safe features, time split, alert budget, per-typology evaluation." |

## 3. The four fraud typologies (know a real-world example of each)

- **ATO (account takeover):** SIM-swap, phishing or screen-sharing apps (AnyDesk-style) → burst of high-value transfers. Signals: new device, velocity, night hours.
- **Mule fan-in:** fake KYC update / "collect request" / lottery scams → many victims pay one account. Signal: payee's distinct new senders in 24h.
- **Credential / VPA testing:** ₹1–10 transactions to check stolen credentials work, then cash-out. Signal: micro-transaction burst.
- **APP scam (authorised push payment):** investment, job or "digital arrest" scams. The customer pays willingly, so device and login look normal. Only behavioural anomalies help, which is why it's the hardest.

## 4. Likely questions & short answers

1. **Why not accuracy?** Imbalance; see §2.
2. **How did you pick the threshold?** Alert budget on a validation window, then reported test results.
3. **What if the fraud rate doubles?** Alert volume changes; re-tune the threshold and monitor precision. The budget is a business constraint.
4. **False positives cost what?** Analyst time plus a blocked genuine customer (complaints, lost trust). That's why precision matters.
5. **How would you deploy it?** Score each txn in real time (milliseconds), with rules and model in parallel; above a high score, block or step-up auth (OTP / call); in a mid band, analyst queue; log outcomes to retrain.
6. **What's your most important feature and why?** Payee history and payee fan-in. Fraud money must land in a mule, so the receiving side is a strong signal.
7. **How do you avoid leakage?** Past-only features and a time split; see §2.
8. **What would you do with real bank data?** Same pipeline, plus device fingerprint, IP/geo, beneficiary-addition events, call-centre and complaint data, and graph features linking mule networks.

## 5. SQL to practise (most fraud analytics tests are SQL)

Practise every query in `sql/fraud_queries.sql` until you can write it from memory:
- `GROUP BY` + `CASE WHEN` (fraud rate by channel)
- self-join on a time range (velocity)
- `AVG() OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)`
- `LAG()` (time since previous txn), `RANK()`/`DENSE_RANK()`/`ROW_NUMBER()` differences
- CTEs (`WITH`), `HAVING`, `COUNT(DISTINCT ...)`
- Classic ones: 2nd-highest value, top-N per group, running total, duplicates, and month-over-month change

## 6. 3-day plan

| Day | Focus |
|---|---|
| **1** | Run TxnVigil end-to-end. Read `features.py` and `train.py` line by line. Explain §2 out loud. SQL: window functions (2 hours, e.g. LeetCode/HackerRank SQL). |
| **2** | Pandas: `groupby`, `merge`, `rolling`, `pivot_table`, handling nulls. ML: precision/recall/PR-AUC, gradient boosting, SHAP (concept only). Power BI: load `transactions.csv`, build 1 page (fraud rate by hour, channel, typology). |
| **3** | Domain: RBI Master Directions on Fraud Risk Management (2024) headline points, AML/KYC basics, recent UPI scam types (I4C/NPCI advisories). Mock interview using §4. Push the repo to GitHub. |

Only keep a skill on the CV if you've done its day: **Power BI** and **RBI Fraud Risk Management directions** are on the IndusInd CV on the assumption you'll do Days 2–3.
