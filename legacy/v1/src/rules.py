"""
Rule engine - the baseline every bank already runs before ML.
Each rule is readable by a fraud analyst / auditor. A txn is flagged if ANY rule fires.
"""
import numpy as np
import pandas as pd

RULES = {
    "R1_NEW_DEVICE_HIGH_AMT": lambda d: (d.device_age_hrs < 1) & (d.user_txn_no > 0) & (d.amt_vs_user_avg > 3),
    "R2_MICRO_TXN_BURST":     lambda d: d.small_txn_1h >= 3,
    "R3_NEW_PAYEE_SPIKE":     lambda d: (d.is_new_payee == 1) & (d.amt_vs_user_avg > 8),
    "R4_PAYEE_FAN_IN":        lambda d: d.payee_new_senders_24h >= 8,
    "R5_NIGHT_VELOCITY":      lambda d: (d.is_night == 1) & (d.user_txn_1h >= 3),
}


def apply_rules(d: pd.DataFrame) -> pd.DataFrame:
    hits = pd.DataFrame({name: fn(d).astype(int) for name, fn in RULES.items()}, index=d.index)
    hits["rule_flag"] = hits.max(axis=1)
    return hits
