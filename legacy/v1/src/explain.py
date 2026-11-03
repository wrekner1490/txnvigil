"""
Reason codes for each alert - so an analyst (and an auditor) can see WHY a txn was flagged.

Method: among the model's most important features, report the ones where this txn's
value is extreme compared with normal (legit) behaviour - beyond the legit 99th
percentile (or below the 1st percentile for "age"-type features). Simple, fast and
explainable; SHAP values are the more exact alternative (see README).
"""
import pandas as pd

TEXT = {
    "payee_txn_no":          "Payee account has very little history",
    "payee_age_hrs":         "Payee account first seen only recently",
    "payee_new_senders_24h": "Many first-time senders paid this payee in 24h (possible mule)",
    "payee_txn_24h":         "Unusual inflow volume to payee in 24h",
    "new_payees_1h":         "Several new payees added within 1 hour",
    "is_new_payee":          "First payment to this payee",
    "amt_vs_user_avg":       "Amount far above customer's usual spend",
    "amt_zscore":            "Amount is a statistical outlier for this customer",
    "user_amt_1h":           "High total amount sent in the last hour",
    "user_txn_1h":           "Many transactions in the last hour",
    "small_txn_1h":          "Burst of Rs.1-10 test transactions",
    "mins_since_last":       "Rapid succession after previous transaction",
    "is_new_device":         "Transaction from a new device",
    "device_age_hrs":        "Device first used very recently",
    "is_night":              "Unusual hour (00:00-05:00)",
}
LOW_IS_RISKY = {"payee_txn_no", "payee_age_hrs", "mins_since_last", "device_age_hrs"}


def reason_codes(row: pd.Series, bundle: dict, top_n: int = 3):
    p99, p01, imp = bundle["legit_p99"], bundle["legit_p01"], bundle["importance"]
    reasons = []
    for f in sorted(imp, key=imp.get, reverse=True):
        if f not in TEXT:
            continue
        v = row[f]
        if f in LOW_IS_RISKY:
            hit = v <= p01[f]
        elif f.startswith("is_"):
            hit = v == 1
        else:
            hit = v > p99[f]
        if hit:
            reasons.append(TEXT[f])
        if len(reasons) == top_n:
            break
    return reasons or ["Combination of moderate risk signals"]
