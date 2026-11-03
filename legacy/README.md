# legacy/

v1 frozen; not maintained; results are v1-only and synthetic.

- v1 was a rules + machine-learning fraud monitoring pipeline for simulated UPI payments: a transaction
  simulator with four fraud typologies, leakage-safe behavioural features, a rule-engine baseline,
  a gradient-boosted model with reason codes, SQL analytics on SQLite, and a Flask + SSE replay dashboard.
- Everything v1 contained is under `legacy/v1/` (`src/`, `templates/`, `sql/`, `reports/`,
  `requirements.txt`, the v1 `README.md` and `INTERVIEW_PREP.md`).
- `legacy/v1/reports/model.joblib` is a historical artefact only. v2 code must never load it (CP-0 C8).
- v2 lives at the repository root; see the root `README.md` and `docs/TXNVIGIL_BUILD_SPEC.md`.
