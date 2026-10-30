"""
Behavioural feature engineering.

RULE: every feature for a transaction uses ONLY information available at the
moment it happens (the customer's / payee's PAST plus the current txn).
Using future data ("leakage") makes offline scores look great and fail in production.
"""
import numpy as np
import pandas as pd

FEATURES = [
    "log_amount", "amt_vs_user_avg", "amt_zscore",
    "hour", "is_night", "is_p2p",
    "is_new_payee", "is_new_device", "device_age_hrs", "user_txn_no", "mins_since_last",
    "user_txn_1h", "user_amt_1h", "user_txn_24h", "small_txn_1h", "new_payees_1h",
    "payee_age_hrs", "payee_txn_no", "payee_txn_24h", "payee_new_senders_24h",
]


def _realign(df, key, s):
    """Rolling results come back ordered by (key, ts); map them back to df's row order."""
    order = df.sort_values([key, "ts"], kind="stable").index
    out = pd.Series(index=order, data=s.values)
    return out.reindex(df.index).values


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ts"] = pd.to_datetime(df["ts"])
    df = df.sort_values("ts", kind="stable").reset_index(drop=True)
    one = np.ones(len(df))

    # --- amount vs the customer's own history (past only -> shift) ---
    la = np.log1p(df["amount"])
    df["log_amount"] = la
    g = df.groupby("user_id", sort=False)
    n_prev = g.cumcount()
    s1 = la.groupby(df.user_id).cumsum() - la
    s2 = (la ** 2).groupby(df.user_id).cumsum() - la ** 2
    mean = (s1 / n_prev.replace(0, np.nan))
    std = np.sqrt((s2 / n_prev.replace(0, np.nan) - mean ** 2).clip(lower=0)) + 0.25
    mean = mean.fillna(np.log1p(400))           # cold start: population typical value
    std = std.fillna(1.0)
    df["amt_vs_user_avg"] = np.expm1(la) / np.expm1(mean)
    df["amt_zscore"] = (la - mean) / std
    df["user_txn_no"] = n_prev

    # --- context ---
    df["hour"] = df.ts.dt.hour
    df["is_night"] = (df.hour < 5).astype(int)
    df["is_p2p"] = (df.channel == "P2P").astype(int)
    df["is_new_payee"] = (~df.duplicated(["user_id", "payee_id"])).astype(int)
    df["is_new_device"] = ((~df.duplicated(["user_id", "device_id"])) & (n_prev > 0)).astype(int)
    df["device_age_hrs"] = (df.ts - df.groupby(["user_id", "device_id"]).ts.transform("min")).dt.total_seconds() / 3600
    df["mins_since_last"] = g.ts.diff().dt.total_seconds().div(60).fillna(7 * 24 * 60)

    # --- velocity (customer side) ---
    df["_one"] = one
    df["_small"] = (df.amount <= 10).astype(int)
    df["user_txn_1h"] = _realign(df, "user_id", _sorted_roll(df, "user_id", "_one", "1h"))
    df["user_amt_1h"] = _realign(df, "user_id", _sorted_roll(df, "user_id", "amount", "1h"))
    df["user_txn_24h"] = _realign(df, "user_id", _sorted_roll(df, "user_id", "_one", "24h"))
    df["small_txn_1h"] = _realign(df, "user_id", _sorted_roll(df, "user_id", "_small", "1h"))
    df["new_payees_1h"] = _realign(df, "user_id", _sorted_roll(df, "user_id", "is_new_payee", "1h"))

    # --- payee side (mule signals) ---
    gp = df.groupby("payee_id", sort=False)
    df["payee_age_hrs"] = (df.ts - gp.ts.transform("min")).dt.total_seconds() / 3600
    df["payee_txn_no"] = gp.cumcount()
    df["payee_txn_24h"] = _realign(df, "payee_id", _sorted_roll(df, "payee_id", "_one", "24h"))
    df["payee_new_senders_24h"] = _realign(df, "payee_id", _sorted_roll(df, "payee_id", "is_new_payee", "24h"))

    return df.drop(columns=["_one", "_small"])


def _sorted_roll(df, key, col, window):
    """Time-window rolling sum per key (includes the current txn)."""
    d = df.sort_values([key, "ts"], kind="stable")
    return (d.set_index("ts").groupby(key, sort=False)[col]
              .rolling(window).sum().reset_index(level=0, drop=True))
