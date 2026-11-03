# TxnVigil v2 — Decision log

Every MASTERMIND verdict and every decision CO-MASTERMIND took alone (ORCHESTRATION_PROMPTS §A.9).
Source of record: CO-MASTERMIND verdict ledger, 2026-11-02. Full RD-1 text: [MASTERMIND_RD-1.md](MASTERMIND_RD-1.md).
Architectural decisions are additionally recorded as ADRs in `docs/adr/`.

Columns: **ID | Date | Decision | Reason / source**

---

## CP-0a (DECISION) — MASTERMIND: APPROVED with directives

| ID | Date | Decision | Reason / source |
|---|---|---|---|
| D-A | 2026-11-02 | WORKER = CO-MASTERMIND's sub-agents, one task at a time; A.6 report + A.7 review always. | CP-0a verdict |
| D-B | 2026-11-02 | Build: dev + unit tests in CO-MASTERMIND cloud workspace; Docker-dependent tests in GitHub Actions on user push; local demo in user's WSL2 (setup task before P4, D9). | CP-0a verdict |
| D-C | 2026-11-02 | Repo = private `wrekner1490/txnvigil`, public at P7. USER does ALL git ops from PowerShell. Workers/CO-MASTERMIND never push, never run git on user's machine, never delete files there. | CP-0a verdict |
| D-D R1 | 2026-11-02 | Drop decisions-table partitioning (was COULD); keep PK(event_id) + alerts FK; index decisions(ts DESC); "monthly partitioning = future". | CP-0a verdict |
| D-D R2 | 2026-11-02 | F02 → `amt_vs_cust_median_recent` = amount / median of customer's last ≤50 payments within 30d. Online: capped list `c:{cid}:amt30` (LPUSH + LTRIM 50, entries "epoch_ms:paise", stale filtered at read). Offline identical → exact parity. `c:{cid}:amt` keeps 8d TTL. | CP-0a verdict |
| D-D R3 | 2026-11-02 | Add feature `cust_txn_cnt_total` (lifetime payment count = Welford n in `c:{cid}:stats`). §11.1 example → `cust_txn_cnt_total > 5`. DSL validator must accept spec's own examples (test). | CP-0a verdict |
| D-D R4 | 2026-11-02 | CI gate 80% coverage on `core/`; 90% a goal. Fix NFR-08 and §18.10 wording. | CP-0a verdict |
| D-D R5 | 2026-11-02 | ML gate baseline = current Production model; before one exists: PR-AUC gate vs logistic regression, recall gate vs rules-only. Write into §17.2. | CP-0a verdict |
| D-D R6 | 2026-11-02 | No third-party dataset files in repo/CI; adapters tested with tiny hand-made schema fixtures; public data in `data/external/` (gitignored), user downloads manually; `make evaluate-public` documents steps. | CP-0a verdict |
| D1 | 2026-11-02 | Delivery protocol: git status check → CO-MASTERMIND writes files → DELIVERY PACKAGE with PowerShell block → CI → "MERGE OK". | CP-0a verdict |
| D2 | 2026-11-02 | Merge only after CI green AND CO-MASTERMIND "MERGE OK". | CP-0a verdict |
| D3 | 2026-11-02 | `.gitattributes` (`* text=auto eol=lf`, binary rules) + `.editorconfig` in P0. | CP-0a verdict |
| D4 | 2026-11-02 | First P0 commit adds `docs/` and moves v1 to `legacy/v1/` with `git mv`. | CP-0a verdict |
| D5 | 2026-11-02 | Scope floor (MUST): simulator v2 + label delay; feature registry + parity tests; LightGBM + LR + rules baselines; graph features; scoring API with rules DSL, policy, reasons, degraded mode; case-service JWT/RBAC/audit; React Live Monitor, Alert Queue, Case View, Rules; CI with ML gates; compose core; ONE public dataset. → SHOULD: 2nd public dataset; Policy what-if page and Models page; champion–challenger; Evidently drift job (simple PSI script = MUST-lite, FR-13a); Isolation Forest; OpenTelemetry; stress/soak perf (smoke + load stay MUST). → COULD: k8s/Helm, Keycloak, GNN, FR-17 export, cosign, mutation testing. | CP-0a verdict |
| D6 | 2026-11-02 | Conventional Commits citing task + requirement IDs; no unproduced result claims. | CP-0a verdict |
| D7 | 2026-11-02 | Spec defaults PROVISIONAL until research; don't pin exact versions beyond what CI needs. | CP-0a verdict |
| D8 | 2026-11-02 | Spec edits only via WORKER tasks citing decision ID. | CP-0a verdict |
| D9 | 2026-11-02 | WSL2 setup guide task before P4. | CP-0a verdict |

---

## CP-0 (PLAN) — MASTERMIND: APPROVED WITH REQUIRED CHANGES

| ID | Date | Decision | Reason / source |
|---|---|---|---|
| P0-T00 | 2026-11-02 | Environment probe ACCEPTED: cloud workspace has py3.12/3.13, uv, ruff, pyright? (n/a), pytest, redis/postgres binaries, node/pnpm; PyPI/npm/Docker Hub/ghcr blocked (403); GitHub API reachable. | CP-0 verdict |
| C1 | 2026-11-02 | Valkey not Redis (compose `valkey/valkey`, smoke `valkey-cli ping`); local redis-server only as stand-in for pure unit tests. | CP-0 verdict |
| C2 | 2026-11-02 | pyright (strict on `core/`) replaces mypy. | CP-0 verdict |
| C3 | 2026-11-02 | PostgreSQL latest stable major image CI can pull (try 18, fall back 17); record tag used. | CP-0 verdict |
| C4 | 2026-11-02 | `requires-python ">=3.12"`; CI matrix 3.12 + 3.13 during P0–P1 + non-blocking deps-probe job (lightgbm, python-igraph, confluent-kafka, duckdb, fastapi, valkey/redis-py, hypothesis, testcontainers); recommend ONE version at CP-1. | CP-0 verdict |
| C5 | 2026-11-02 | T02 scope = D-D R1–R6 + D5 + FR-13a + ALL RD-1 §2 items 1–10; add `docs/RESEARCH.md` + `docs/MASTERMIND_RD-1.md` to DLV-1. | CP-0 verdict |
| C6 | 2026-11-02 | ADRs Accepted: 0001 Redpanda (dev-container mode) over Kafka; 0002 Valkey + hand-rolled Lua feature store over Feast and Redis (licence + latency); 0003 LightGBM single GBDT family (no XGBoost shadow), unweighted training + isotonic calibration, pred_contrib reason codes; 0004 own JWT + RBAC over Keycloak; 0005 pyright + ruff + uv toolchain. Monorepo = ADR-0006 (P1). No version pins in ADRs. | CP-0 verdict |
| C7 | 2026-11-02 | `git add --renormalize .` in T01 block; AC `git ls-files --eol` shows no w/crlf for text. | CP-0 verdict |
| C8 | 2026-11-02 | `legacy/v1/reports/model.joblib` excluded from any future loading code (may stay in git); `legacy/README.md`: "v1 frozen; not maintained; results are v1-only and synthetic". | CP-0 verdict |
| D-E | 2026-11-02 | Option B default (CI = test runner for third-party deps; pure-Python pre-checked locally). Option A is the user's choice (allow registries in Claude code-execution network settings → re-run T00 step 3). Escalation: >2 CI-fix rework rounds (-R2) on any task → pull D9 WSL2 setup forward (option C), report in next checkpoint. | CP-0 verdict |
| D-F | 2026-11-02 | DLV-1 = T01 + T02 + T06, DLV-2 = T03 + T04, DLV-3 = T05. | CP-0 verdict |
| K2 | 2026-11-02 | pyproject lower bounds only; CI job `lock` runs `uv lock` and uploads uv.lock artefact; user commits it in DLV-2-R or DLV-3; then CI uses `uv sync --frozen`. Same for pnpm-lock.yaml in P5. | CP-0 verdict |
| 9a | 2026-11-02 | MUST count 15 FR (FR-01..10, 12, 14 [narrowed: simulator + ONE public dataset], 15, 16, FR-13a PSI script MUST-lite) + 10 NFR; re-classification approved (FR-11 SHOULD, FR-13 SHOULD, US-04 what-if UI SHOULD with policy API MUST, US-09/FR-17 COULD, US-10 via FR-13a). | CP-0 verdict |
| 9b | 2026-11-02 | Cut order: 1 COULD items; 2 Isolation Forest; 3 OpenTelemetry; 4 stress+soak perf; 5 Evidently (PSI stays); 6 champion–challenger (manual promote stays); 7 Models page; 8 Policy what-if page (API stays); 9 second public dataset. Never cut past D5 floor → slip + escalate. | CP-0 verdict |
| T04 | 2026-11-02 | Traceability gate warn-only through P1, failing from P2. | CP-0 verdict |
| 9d | 2026-11-02 | Repo setup approved; add no-secrets check `git ls-files \| Select-String -Pattern "\.env$\|secret\|key"` before first push; recommend Option 2 (github.com + git remote add) unless `gh --version` works. | CP-0 verdict |

---

## RD-1 — Research decisions — ACCEPTED WITH MODIFICATIONS (binding)

Input: `docs/RESEARCH.md` (research report received 2026-11-02). RD-1 resolves every [R#] marker in the
spec and overrides the research wherever they differ. Full text: [MASTERMIND_RD-1.md](MASTERMIND_RD-1.md).

### §0 Research trust policy

| ID | Date | Decision | Reason / source |
|---|---|---|---|
| RD-1 §0 | 2026-11-02 | Research is an input, not a source of truth. Research version numbers are reference points only (pin what the resolver installs; image tags CI can pull). No research statistic or legal fact goes into README, user-facing docs, UI or CV until its primary source is opened and confirmed; unverified items marked `UNVERIFIED`. Third-party benchmark numbers are never quoted as TxnVigil results. | RD-1 §0 (MASTERMIND spot-checked 5 claims: 3 confirmed, 1 corrected — Oracle ARM cut date 2026-08-18 — 1 weakly supported — ₹5,000/24h new-device limit) |

### §1 [R#] resolutions

| ID | Date | Decision | Priority | Reason / source |
|---|---|---|---|---|
| RD-1 #1 | 2026-11-02 | Case schema gets compliance timestamps (occurred_at, detected_at, red_flagged_at, classified_fraud_at) + reporting deadlines computed from a config table (defaults from RBI fraud directions / FIU-IND with source URL); SCN workflow = optional case sub-state, not on payment path. | MUST-lite (fields + deadlines) | RD-1 §1, R1 regulation |
| RD-1 #1b | 2026-11-02 | "FMR-like" / "STR-like" JSON exports are illustrative, labelled "not an official RBI/FIU-IND format"; no FINnet compatibility claim. | COULD | RD-1 §1, R1 exports |
| RD-1 #1c | 2026-11-02 | `/v1/score` caller response carries only action + generic customer-safe message code; reasons, rules, scores only to internal topics and analyst UI (caller view vs internal decision record). | MUST | RD-1 §1, R1 tipping-off |
| RD-1 #1d | 2026-11-02 | IDs pseudonymised with keyed HMAC (key from env); no PII unmask needed; every case view/export audited. | MUST | RD-1 §1, R1 DPDP |
| RD-1 #1e | 2026-11-02 | Pre-ML policy rules as configurable YAML rules: new-device cooling limit (default ₹5,000/24h, marked "verify"), P2P collect = blocked (confirmed), payee negative-list match. | MUST | RD-1 §1, R1 NPCI rules |
| RD-1 #2 | 2026-11-02 | Dual-sided (payer + payee) features; simulator adds digital arrest, task/job scam, APK/screen-share takeover, 2–3 hop mule layering (plus v1's four). | MUST | RD-1 §1, R2 typologies |
| RD-1 #2b | 2026-11-02 | `is_call_active`, `is_screen_sharing`, `qr_source`, `fd_broken_1h` only as simulator fields documented "assumes PSP app SDK telemetry"; model also evaluated without them (ablation). | SHOULD | RD-1 §1, R2 device telemetry |
| RD-1 #3 | 2026-11-02 | Public benchmark #1 IBM AMLworld HI-Small (MUST); #2 IEEE-CIS (SHOULD); SAML-D COULD; PaySim and ULB not used for headline results (documented "why not" only); licences checked and recorded in `docs/data_sheet.md`. | MUST/SHOULD | RD-1 §1, R3 datasets |
| RD-1 #4 | 2026-11-02 | Model A LightGBM transaction classifier, unweighted + isotonic calibration (one class-weighted ablation); Model B LightGBM account mule classifier (graph + behavioural, micro-batch, writes `mule_prob` online); Model C Isolation Forest as feature + drift signal; no XGBoost shadow; champion/challenger = two LightGBM versions. | A MUST, B SHOULD (MUST if P3 on time), C SHOULD | RD-1 §1, R4 models |
| RD-1 #5 | 2026-11-02 | 3-stage pipeline (pre-ML rules → model + reasons → policy) with 50 ms circuit breaker to rules-only; feature log-and-wait (each decision publishes its exact feature vector → Parquet; training uses logged vectors where available). | MUST | RD-1 §1, R5 architecture |
| RD-1 #5b | 2026-11-02 | Latency targets p50 ≤ 15 ms, p99 ≤ 50 ms at 200 RPS on a laptop (was 100 ms); stretch 15 ms p99; no hard latency gate on GitHub-hosted runners; CI smoke perf p99 ≤ 250 ms; real numbers from `make perf` on user's machine with hardware notes. | MUST | RD-1 §1, R5 latency |
| RD-1 #6 | 2026-11-02 | Valkey (BSD-3) instead of Redis, same client libraries; hand-rolled feature store with atomic Lua scripts; Feast not used. | MUST | RD-1 §1, R6 online store |
| RD-1 #6b | 2026-11-02 | Redpanda dev-container mode (smp 1, memory capped); plain `confluent-kafka` consumers; no Bytewax/Faust/Flink. | MUST | RD-1 §1, R6 broker/consumer |
| RD-1 #6c | 2026-11-02 | PostgreSQL (latest stable image CI pulls); DuckDB + Parquet offline store with ASOF joins for point-in-time training sets. | MUST | RD-1 §1, R6 storage |
| RD-1 #6d | 2026-11-02 | Core compose profile = 6 containers (valkey, redpanda, postgres, scoring-api, stream-worker, web) with explicit `mem_limit`s, target ≤ 3.5 GB under load; MLflow/MinIO only in `mlops` profile. | MUST | RD-1 §1, R6 compose |
| RD-1 #7 | 2026-11-02 | Online reason codes from LightGBM `pred_contrib=True` (no `shap` on hot path; `shap` offline for plots only); reason-code dictionary RC01–RCnn with templates. | MUST | RD-1 §1, R7 explainability |
| RD-1 #7b | 2026-11-02 | MODEL_CARD.md, DATASHEET.md, mapping table to RBI FREE-AI recommendations (cited from primary report URL); subgroup FPR/alert-rate parity across synthetic segments; AIBOM (CERT-In) COULD. | SHOULD | RD-1 §1, R7 governance |
| RD-1 #8 | 2026-11-02 | Production scorecard module: VDR, ADR, AFR (FP:TP), precision@K / alert budget, friction rate, time-to-detect, net savings ₹ (stated cost assumptions); VDR-vs-alert-volume curve in evaluation report and UI. | MUST | RD-1 §1, R8 metrics |
| RD-1 #8b | 2026-11-02 | Rule backtester reports total hits, incremental TP/FP vs champion model, marginal AFR, ₹ captured. | MUST | RD-1 §1, R8 backtester |
| RD-1 #9 | 2026-11-02 | `python-igraph` micro-batch graph job (every 5 min in demo, configurable): in/out degree, pass-through ratio, median dwell time, PageRank, personalised fraud PageRank (labels available at batch time only), Leiden community fraud rate, 3-cycle flag, shared-device degree; NetworkX only for UI ego-graphs; PyG GNN ablation COULD. | MUST (GNN COULD) | RD-1 §1, R9 graph |
| RD-1 #10 | 2026-11-02 | uv + ruff + pyright (replaces mypy; strict on `core/`); JS pnpm, Vite, Vitest, Playwright; CI per research §R10(c) except ZAP baseline nightly, cosign COULD, OIDC only with a cloud (none until P7); scans: gitleaks, osv-scanner (or pip-audit), bandit, Trivy, Syft SBOM. | MUST (ZAP SHOULD) | RD-1 §1, R10 tooling |
| RD-1 #11 | 2026-11-02 | Primary hosting Oracle Cloud Always Free ARM (2 OCPU / 12 GB after 2026-08-18), Indian region if available → all images multi-arch (amd64 + arm64), checked in CI with buildx; secondary GitHub Codespaces devcontainer; HF Spaces single-container demo COULD. | SHOULD (P7) | RD-1 §1, R11 hosting |
| RD-1 #12 | 2026-11-02 | Simulator in plain Python/NumPy discrete-event generator (no Mesa/SimPy unless a need is shown); realism checks: amount KS vs AMLworld, IST diurnal profile, degree power-law fit, Benford, balance conservation, TSTR rank correlation vs AMLworld; SDMetrics if it installs cleanly, else SciPy. | MUST (checks), SHOULD (SDMetrics) | RD-1 §1, R12 synthetic data |
| RD-1 #13 | 2026-11-02 | README positioning vs Marble, ezrules, Jube, Tazama (verify each repo's current state first); adopt the research's 5 differentiators minus any claim not backed by repo output. | SHOULD (P7) | RD-1 §1, R13 positioning |

### §2 Spec changes

| ID | Date | Decision | Reason / source |
|---|---|---|---|
| RD-1 §2 | 2026-11-02 | CO-MASTERMIND applies RD-1 to the spec via a P0 WORKER task (items 1–10: replace [R#] markers citing "RD-1 #n"; §5/§6.2 typologies + telemetry fields; §7 Valkey rename, circuit breaker, log-and-wait, caller/internal split; §4.5 NFR-01 + §18.7 latency; §9 dual-sided + graph features, no fixed feature count; §10 models A/B/C, isotonic, pred_contrib; §14.1 compliance timestamps + `compliance_deadlines` table, audit of case views/exports; §17 pyright, ZAP nightly, multi-arch; add `docs/RESEARCH.md` with `UNVERIFIED` tags; record RD-1 here). Executed as P0-T02 (CP-0 C5). | RD-1 §2, §4 |

### §3 Not adopted

| ID | Date | Decision | Reason / source |
|---|---|---|---|
| RD-1 §3a | 2026-11-02 | "<15 ms p99" not a requirement — stretch goal only. | Unrealistic as a hard gate for Python + Valkey round-trips on shared CI hardware (RD-1 §3) |
| RD-1 §3b | 2026-11-02 | No XGBoost shadow model. | Adds a dependency without adding a different signal (RD-1 §3) |
| RD-1 §3c | 2026-11-02 | No Feast. | Not needed at this scale; adds latency and complexity (RD-1 §3) |
| RD-1 §3d | 2026-11-02 | No Mesa/SimPy. | Unnecessary for the simulator's needs (RD-1 §3) |
| RD-1 §3e | 2026-11-02 | No official-format regulatory exports. | No official schemas available; illustrative only (RD-1 §3) |
| RD-1 §3f | 2026-11-02 | No fixed feature count (45). | Feature count follows the registry, not a target number (RD-1 §3) |

### §4 Impact on P0

| ID | Date | Decision | Reason / source |
|---|---|---|---|
| RD-1 §4 | 2026-11-02 | P0 gains one task (spec update per §2). T00 probe also checks Python 3.13 wheels for lightgbm, python-igraph, confluent-kafka, duckdb (use 3.13 if all install, else 3.12) and that valkey, redpanda and postgres images pull. CP-0 must reflect RD-1. | RD-1 §4 |

---

## CO-MASTERMIND decisions (taken alone)

| ID | Date | Decision | Reason / source |
|---|---|---|---|
| CM-01 | 2026-11-02 | RESEARCH.md: rather than tagging every statistic, add a prominent note that the report's own "Verified Fact" labels are the research author's, not MASTERMIND's; only the items listed in RD-1 §0 are confirmed; everything else UNVERIFIED (existing header already says so). Individual statistics get an inline `UNVERIFIED` tag only when they are quoted into the spec. | CO-MASTERMIND, applying RD-1 §0 / §2 item 9 |
| CM-02 | 2026-11-02 | DLV-1 is prepared in the cloud workspace and written to `D:\cv\txnvigil` only after the user's `git status` confirms a clean main (D1a). | CO-MASTERMIND, applying CP-0a D1 / D-C |
| CM-03 | 2026-11-02 | `.gitignore`: v1's `data/` rule anchored to `/data/` (and `/data/external/`) so test fixtures or `web/src/data` folders are not silently ignored. | CO-MASTERMIND, P0-T01 review (A.3: file layout) |
| CM-04 | 2026-11-03 | `services/stream_worker/` directory name follows RD-1 #6d service rename (resolves spec OI-3 naming for services; `adapters/paysim.py` not created per RD-1 #3). | CO-MASTERMIND, P0-T03 (A.3 naming/layout) |
