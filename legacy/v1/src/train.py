"""
Train + evaluate the fraud model and compare it with the rule engine.

  * time-based split (train on the past, test on the future) - never a random split
  * gradient-boosted trees with class weighting for the ~0.4% fraud rate
  * alert threshold chosen on a validation window for a fixed alert budget
  * metrics a fraud team cares about: PR-AUC, recall, precision, false-positive rate,
    alerts per day, % of fraud VALUE caught, recall per fraud typology

Usage:  python src/train.py
"""
import json
import sys
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).parent))
from features import FEATURES, build_features
from rules import apply_rules

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
ALERT_BUDGET = 0.005        # analysts can review 0.5% of transactions


def split(df):
    day = (df.ts - df.ts.min()).dt.days
    return df[day < 40], df[(day >= 40) & (day < 48)], df[day >= 48]


def evaluate(name, y, flag, score, frame):
    tp = int(((flag == 1) & (y == 1)).sum()); fp = int(((flag == 1) & (y == 0)).sum())
    fn = int(((flag == 0) & (y == 1)).sum())
    days = frame.ts.dt.normalize().nunique()
    fraud_val = frame.amount[y == 1].sum()
    res = {
        "model": name,
        "pr_auc": round(float(average_precision_score(y, score)), 4) if score is not None else None,
        "roc_auc": round(float(roc_auc_score(y, score)), 4) if score is not None else None,
        "precision": round(tp / max(tp + fp, 1), 4),
        "recall": round(tp / max(tp + fn, 1), 4),
        "false_positive_rate": round(fp / max(int((y == 0).sum()), 1), 5),
        "alerts_per_day": round((tp + fp) / days, 1),
        "fraud_value_caught_pct": round(100 * frame.amount[(flag == 1) & (y == 1)].sum() / fraud_val, 2),
        "recall_by_typology": {
            t: round(float(flag[(frame.fraud_type == t).values].mean()), 3)
            for t in sorted(frame.fraud_type[y == 1].unique())
        },
    }
    print(f"\n== {name} ==")
    for k, v in res.items():
        if k != "model":
            print(f"  {k:24s} {v}")
    return res


def main():
    data = ROOT / "data" / "transactions.csv"
    print("building features ...")
    df = build_features(pd.read_csv(data))
    tr, va, te = split(df)
    print(f"train {len(tr):,} | valid {len(va):,} | test {len(te):,}  (fraud in test: {te.is_fraud.sum()})")

    # ---- 1. rule engine baseline ----
    results = [evaluate("Rule engine (baseline)", te.is_fraud.values,
                        apply_rules(te).rule_flag.values, None, te)]

    # ---- 2. logistic regression (simple ML baseline) ----
    w = np.where(tr.is_fraud == 1, (tr.is_fraud == 0).sum() / tr.is_fraud.sum(), 1.0)
    lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    lr.fit(tr[FEATURES], tr.is_fraud, logisticregression__sample_weight=w)

    # ---- 3. gradient-boosted trees ----
    gbt = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.08, max_leaf_nodes=31,
                                         l2_regularization=1.0, class_weight="balanced", random_state=7)
    gbt.fit(tr[FEATURES], tr.is_fraud)

    models = {"Logistic regression": lr, "Gradient-boosted trees": gbt}
    thresholds = {}
    for name, m in models.items():
        # threshold = score at which 0.5% of VALIDATION txns would be alerted
        thr = float(np.quantile(m.predict_proba(va[FEATURES])[:, 1], 1 - ALERT_BUDGET))
        thresholds[name] = thr
        s = m.predict_proba(te[FEATURES])[:, 1]
        results.append(evaluate(name, te.is_fraud.values, (s >= thr).astype(int), s, te))

    # ---- hybrid: rules OR model (how banks deploy in practice) ----
    s = gbt.predict_proba(te[FEATURES])[:, 1]
    hybrid = ((s >= thresholds["Gradient-boosted trees"]) | (apply_rules(te).rule_flag.values == 1)).astype(int)
    results.append(evaluate("Hybrid (rules OR GBT)", te.is_fraud.values, hybrid, None, te))

    # ---- explainability: permutation importance (drop in PR-AUC when a feature is shuffled) ----
    samp = te.sample(150_000, random_state=1) if len(te) > 150_000 else te
    samp = pd.concat([samp, te[te.is_fraud == 1]]).drop_duplicates("txn_id")
    pi = permutation_importance(gbt, samp[FEATURES], samp.is_fraud, scoring="average_precision",
                                n_repeats=3, random_state=0, n_jobs=1)
    imp = pd.Series(pi.importances_mean, index=FEATURES).sort_values(ascending=False)

    # ---- save artefacts ----
    REPORTS.mkdir(exist_ok=True)
    legit = tr[tr.is_fraud == 0]
    joblib.dump({"model": gbt, "threshold": thresholds["Gradient-boosted trees"], "features": FEATURES,
                 "legit_p99": legit[FEATURES].quantile(0.99).to_dict(),
                 "legit_p01": legit[FEATURES].quantile(0.01).to_dict(),
                 "importance": imp.to_dict()}, ROOT / "reports" / "model.joblib")
    summary = {"dataset": {"transactions": int(len(df)), "fraud": int(df.is_fraud.sum()),
                           "fraud_rate_pct": round(100 * df.is_fraud.mean(), 3),
                           "train": len(tr), "valid": len(va), "test": len(te),
                           "test_fraud": int(te.is_fraud.sum())},
               "alert_budget_pct": 100 * ALERT_BUDGET,
               "results": results,
               "feature_importance": imp.round(4).to_dict()}
    (REPORTS / "metrics.json").write_text(json.dumps(summary, indent=2))
    # test window with features, replayed by the live dashboard (app.py)
    te[["txn_id", "ts", "user_id", "payee_id", "amount", "channel", "is_fraud", "fraud_type"] + FEATURES] \
        .to_pickle(ROOT / "data" / "stream.pkl")

    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    for name, m in models.items():
        p, r, _ = precision_recall_curve(te.is_fraud, m.predict_proba(te[FEATURES])[:, 1])
        ax[0].plot(r, p, label=f"{name} (PR-AUC {average_precision_score(te.is_fraud, m.predict_proba(te[FEATURES])[:, 1]):.3f})")
    rb = results[0]
    ax[0].scatter([rb["recall"]], [rb["precision"]], c="k", zorder=5, label="Rule engine")
    ax[0].set_xlabel("Recall"); ax[0].set_ylabel("Precision"); ax[0].set_title("Precision-Recall (test window)")
    ax[0].legend(); ax[0].grid(alpha=.3)
    imp.head(12)[::-1].plot.barh(ax=ax[1], color="#3b6ea5")
    ax[1].set_title("Permutation importance (drop in PR-AUC)")
    plt.tight_layout(); plt.savefig(REPORTS / "model_report.png", dpi=130)
    print("\nsaved reports/metrics.json, reports/model_report.png, reports/model.joblib")


if __name__ == "__main__":
    main()
