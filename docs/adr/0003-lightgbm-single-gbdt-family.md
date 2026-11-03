# ADR-0003: LightGBM as the single GBDT family

- **Status:** Accepted
- **Date:** 2026-11-02
- **Deciders:** MASTERMIND (decision), CO-MASTERMIND (record)

## Context

TxnVigil needs a transaction classifier (model A) and an account mule classifier (model B) on tabular and
graph features, with calibrated probabilities for a cost-sensitive policy and per-decision reason codes on
the hot path (spec §10, §8.5, §8.6). Fraud labels are heavily imbalanced. We want one well-understood
model family rather than several overlapping ones.

## Decision

- **LightGBM** is the only gradient-boosted tree family. **No XGBoost shadow model.**
  Champion/challenger compares **two LightGBM versions**.
- Train **unweighted**, then apply **isotonic calibration**. A class-weighted variant is compared **once**,
  in an ablation, and the result is reported as found.
- **Online reason codes** come from LightGBM's own `pred_contrib=True` (native TreeSHAP), mapped to the
  reason-code dictionary (RC01–RCnn).
- The **`shap` library is offline only** (plots, reports); it never runs on the scoring path.
- Logistic regression and rules-only remain as baselines (D5), not as competing GBDTs.

## Consequences

### Positive

- One dependency, one hyper-parameter vocabulary, one model-packaging path.
- Calibrated probabilities make policy thresholds and expected-cost reasoning meaningful.
- Native contributions avoid an extra library and its latency on the hot path.

### Negative

- No cross-family check: errors specific to LightGBM's tree-building are not caught by a second family.
- Isotonic calibration needs a held-out calibration split and can overfit if that split is small.
- `pred_contrib` values explain the raw margin, not the calibrated probability; reason-code text must be
  worded with that in mind.
- Any LightGBM bug or breaking change affects both models A and B at once.

### Follow-ups

- Ablation: unweighted + isotonic vs class-weighted, reported in the evaluation report.
- Test that online `pred_contrib` reasons match offline `shap` attributions on sample events.
- Record the LightGBM version from the lockfile in the model card; no pin here.

## Alternatives considered

| Option | Why not chosen |
|---|---|
| XGBoost shadow model | Adds a dependency without adding a different signal (RD-1 §3). |
| CatBoost | Same family of model, no clear benefit for our features; one GBDT family is enough. |
| Class-weighted training as default | Distorts probabilities; kept only as a one-off ablation (RD-1 #4). |
| `shap` library online | Extra dependency and latency for what `pred_contrib` gives natively (RD-1 #7). |

Rationale wording per RESEARCH.md R4 (UNVERIFIED); no third-party benchmark figures are claimed.

## References

- RD-1 #4 (models), RD-1 #7 (explainability), RD-1 §3 (XGBoost not adopted)
- CP-0 C6 (ADRs accepted, no version pins), D5 (baselines in scope floor)
- Spec §7.4, §8.6, §10.1, §10.4
