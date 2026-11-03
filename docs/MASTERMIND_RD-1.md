# MASTERMIND DIRECTIVE RD-1 — Research decisions for TxnVigil v2

Input: `docs/RESEARCH.md` (Gemini research report, 13 sections + decisions table), received 2026-11-02.
Status: **ACCEPTED WITH MODIFICATIONS.** This directive resolves every [R#] marker in the spec and
overrides the research wherever they differ. CO-MASTERMIND applies it to the spec through a WORKER task
(P0), citing "RD-1 / item #".

## 0. Research trust policy (applies to everything below)
- The research is an **input, not a source of truth**. MASTERMIND spot-checked 5 high-impact claims:
  - Confirmed: NPCI ended P2P collect requests from 2025-10-01; RBI Master Directions on Fraud Risk
    Management (July 2024) exist; LightGBM 4.7.0 exists.
  - Corrected: Oracle Always Free ARM cut to 2 OCPU / 12 GB takes effect **2026-08-18** (not June).
  - Weakly supported: the "₹5,000 in first 24h on a new device" limit is reported by bank/fintech sources
    but not confirmed from an NPCI primary document → it is a configurable policy default, not a hard rule.
- **Versions:** the research's exact version numbers are reference points only. The WORKER pins whatever
  the resolver actually installs (uv.lock, pnpm-lock.yaml) and uses image tags that CI can pull. If a
  quoted version doesn't exist, use the latest stable and note it. Never pin from the report without an
  install succeeding.
- **Statistics and legal facts:** nothing from the research goes into README, docs shown to users, the UI or
  the CV until someone has opened the primary source URL and confirmed it. Mark unverified items
  `UNVERIFIED` in docs/RESEARCH.md.
- Benchmark numbers from third-party papers (e.g. "LightGBM 0.807 F1 vs GNN 0.439") must never be quoted
  as TxnVigil results.

## 1. [R#] resolutions
| # | Area | Decision | Priority |
|---|---|---|---|
| 1 | R1 regulation | Case schema gets compliance timestamps: occurred_at, detected_at, red_flagged_at, classified_fraud_at, plus computed reporting deadlines from a **config table** (default values from the RBI fraud directions / FIU-IND as cited in RESEARCH.md, each with source URL). The SCN (show-cause) workflow applies to classifying a *person/entity* as fraudulent, so it is modelled as an optional case sub-state, not on the payment path. | MUST-lite (fields + deadlines) |
| 1b | R1 exports | "FMR-like" and "STR-like" JSON exports are **illustrative**, labelled "not an official RBI/FIU-IND format". No claim of FINnet compatibility. | COULD |
| 1c | R1 tipping-off | The `/v1/score` response to the payment caller carries only the action + a generic customer-safe message code. Reasons, rules and scores go only to internal topics and the analyst UI. API split: `/v1/score` (caller view) vs. internal decision record. | MUST |
| 1d | R1 DPDP | IDs pseudonymised with keyed HMAC (key from env); PII unmask is not needed (synthetic data has no PII), but every case view/export is audited. | MUST |
| 1e | R1 NPCI rules | Pre-ML policy rules shipped as **configurable** rules in the YAML ruleset: new-device cooling limit (default ₹5,000/24h, marked "verify"), P2P collect = blocked (confirmed), payee negative-list match. | MUST |
| 2 | R2 typologies | Adopt **dual-sided features** (payer + payee). Add typologies to the simulator: digital arrest, task/job scam, APK/screen-share takeover, 2–3 hop mule layering (in addition to v1's four). | MUST |
| 2b | R2 device-telemetry features | `is_call_active`, `is_screen_sharing`, `qr_source`, `fd_broken_1h` are allowed **only as simulator-generated fields documented as "assumes PSP app SDK telemetry"**. The model must also be evaluated *without* them (ablation), so results don't depend on data a bank may not have. | SHOULD |
| 3 | R3 datasets | Public benchmark #1 (MUST): **IBM AMLworld HI-Small** (graph/mule). #2 (SHOULD): **IEEE-CIS** (device/velocity). SAML-D: COULD. PaySim and ULB: not used for headline results (leakage / PCA) — can appear only as a documented "why not". Check each licence before use and record it in docs/data_sheet.md. | MUST/SHOULD |
| 4 | R4 models | Model A: LightGBM transaction classifier, **unweighted training + isotonic calibration** (compare once against class-weighted in an ablation). Model B: LightGBM **account mule classifier** on graph + behavioural features, micro-batch, writes `mule_prob` to the online store. Model C: Isolation Forest score as a feature + drift signal. XGBoost shadow: not adopted (one GBDT family is enough); champion/challenger uses two LightGBM versions. | A MUST, B SHOULD (MUST if P3 on time), C SHOULD |
| 5 | R5 architecture | 3-stage pipeline (pre-ML rules → model + reasons → policy) with **circuit breaker 50 ms** to rules-only. **Feature log-and-wait:** every decision publishes the exact feature vector used → Parquet; training uses logged vectors where available (zero train/serve skew). | MUST |
| 5b | R5 latency | Targets: p50 ≤ 15 ms, **p99 ≤ 50 ms** at 200 RPS on a laptop (was 100 ms). Stretch 15 ms p99. **No hard latency gate on GitHub-hosted runners** (noisy); CI runs a smoke perf test with a generous threshold (p99 ≤ 250 ms); the real numbers come from `make perf` on the user's machine and are recorded with hardware notes. | MUST |
| 6 | R6 online store | **Valkey** (BSD-3) instead of Redis, same client libraries. Hand-rolled feature store with **atomic Lua** read/update scripts. **Feast not used.** | MUST |
| 6b | R6 broker/consumer | Redpanda in dev-container mode (smp 1, memory capped); `confluent-kafka` plain consumers. No Bytewax/Faust/Flink. | MUST |
| 6c | R6 storage | PostgreSQL (major version = latest stable image that CI pulls), DuckDB + Parquet offline store with ASOF joins for point-in-time training sets. | MUST |
| 6d | R6 compose | Core profile = 6 containers (valkey, redpanda, postgres, scoring-api, stream-worker, web) with explicit `mem_limit`s; target ≤ 3.5 GB under load. MLflow/MinIO only in `mlops` profile. | MUST |
| 7 | R7 explainability | Online reason codes from LightGBM **`pred_contrib=True`** (native TreeSHAP; no `shap` library on the hot path). `shap` only offline for plots. Reason-code dictionary RC01–RCnn with templates. | MUST |
| 7b | R7 governance | MODEL_CARD.md, DATASHEET.md, and a mapping table to the RBI FREE-AI recommendations (sutras/recommendations cited from the primary report URL). Subgroup FPR/alert-rate parity across synthetic customer segments. AIBOM (CERT-In): COULD. | SHOULD |
| 8 | R8 metrics | Production scorecard module: VDR, ADR, AFR (FP:TP), precision@K / alert budget, friction rate, time-to-detect, net savings ₹ (with stated cost assumptions). VDR-vs-alert-volume curve in evaluation report and UI. | MUST |
| 8b | R8 backtester | Rule backtester reports total hits, **incremental** TP/FP vs the champion model, marginal AFR, ₹ captured. | MUST |
| 9 | R9 graph | `python-igraph` for the micro-batch graph job (every 5 min in demo; configurable): in/out degree, pass-through ratio, median dwell time, PageRank, personalised fraud PageRank (seeded only with labels available at batch time), Leiden community fraud rate, 3-cycle flag, shared-device degree. NetworkX only for UI ego-graphs if needed. PyG GNN ablation: COULD. | MUST (GNN COULD) |
| 10 | R10 tooling | Python: uv + ruff + **pyright** (replaces mypy; strict on `core/`). JS: pnpm, Vite, Vitest, Playwright. CI workflows as research §R10(c), with these changes: ZAP baseline runs **nightly**, not per-PR; cosign signing COULD; OIDC only where a cloud is involved (none until P7). Security scans: gitleaks, osv-scanner (or pip-audit), bandit, Trivy, Syft SBOM. | MUST (ZAP SHOULD) |
| 11 | R11 hosting | Primary: **Oracle Cloud Always Free ARM (2 OCPU / 12 GB after 2026-08-18)** in an Indian region if capacity is available → all images must be **multi-arch (amd64 + arm64)**, checked in CI with buildx. Secondary: **GitHub Codespaces devcontainer** (no card needed for reviewers). HF Spaces single-container demo: COULD. | SHOULD (P7) |
| 12 | R12 synthetic data | Simulator: plain Python/NumPy discrete-event generator (no Mesa/SimPy dependency unless the WORKER shows a need). Realism checks: amount distribution vs AMLworld (KS), diurnal profile in IST, degree distribution (power-law fit), Benford first-digit check, balance conservation, TSTR rank correlation against AMLworld. SDMetrics: allowed if it installs cleanly; otherwise SciPy implementations. | MUST (checks), SHOULD (SDMetrics) |
| 13 | R13 positioning | README positioning vs Marble, ezrules, Jube, Tazama (verify each repo's current state before any comparison claim). Adopt the research's 5 differentiators, minus any claim not backed by repo output. | SHOULD (P7) |

## 2. Spec changes CO-MASTERMIND must make (via a P0 WORKER task "P0-Tnn spec-update-RD-1")
1. Replace every [R#] marker with the decision above (cite "RD-1 #n").
2. §5 and §6.2: add the new typologies (2) and device-telemetry fields (2b).
3. §7: rename Redis → Valkey throughout; add the circuit breaker and feature log-and-wait flow; split
   caller response vs. internal decision record (1c).
4. §4.5 NFR-01: new latency targets (5b); §18.7 updated accordingly.
5. §9: add the dual-sided payee features and the graph feature list (9); keep the count driven by the registry
   (no fixed "45 features" target).
6. §10: models A/B/C (4), unweighted + isotonic calibration, pred_contrib reasons (7).
7. §14.1: add compliance timestamp columns + `compliance_deadlines` config table (1); `audit_log` covers
   case views/exports (1d).
8. §17: pyright instead of mypy; ZAP nightly; multi-arch builds (11).
9. Add `docs/RESEARCH.md` (the converted report) with `UNVERIFIED` tags on any statistic not yet checked.
10. Record RD-1 in docs/DECISIONS.md.

## 3. Not adopted (and why)
- **"<15 ms p99" as a requirement:** unrealistic as a hard gate for Python + Valkey round-trips on shared
  CI hardware. Kept as a stretch goal only.
- **XGBoost shadow model:** adds a dependency without adding a different signal.
- **Feast:** not needed at this scale; adds latency and complexity.
- **Mesa/SimPy:** unnecessary for the simulator's needs.
- **Official-format regulatory exports:** we have no official schemas; illustrative only.
- **Fixed feature count (45):** feature count follows the registry, not a target number.

## 4. Impact on P0
- P0 gains one task: spec update per §2 above.
- T00 environment probe must also check: Python 3.13 wheels for lightgbm, python-igraph, confluent-kafka,
  duckdb (use 3.13 if all install, else 3.12), and that valkey, redpanda and postgres images pull.
- CP-0 (PLAN) is still expected next; it must reflect RD-1.
