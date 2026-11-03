# Research Brief for TxnVigil v2 (paste everything below the line into the research model)

---

You are a senior research analyst. I am building **TxnVigil v2**, an open-source, real-time transaction-risk
and mule-detection platform for **UPI-style payments in India** (portfolio project; no real customer data).
Stack direction: Python (FastAPI, LightGBM, SHAP), Redis online features, Redpanda/Kafka, PostgreSQL,
DuckDB/Parquet, MLflow, React + TypeScript, Docker Compose, GitHub Actions. It must run on a laptop
with 8–16 GB RAM using only free/open-source tools.

Research the 13 topics below. **Rules for every answer:**
1. Use sources dated **2023 or later** wherever possible; give the **publication date** for every source.
2. Give a **direct URL** for every factual claim. Prefer primary sources (RBI, NPCI, MeitY, Gazette,
   official docs, peer-reviewed papers, official GitHub repos, company engineering blogs).
3. Separate **verified facts** from **your inference**. Mark uncertain items with `UNCERTAIN`.
4. Give **exact versions** of software as of the latest stable release you can find, with the release date.
5. Do not invent statistics, circular numbers, paper titles or URLs. If not found, say "not found".
6. Output format per topic: **(a) 5-line summary, (b) key facts table with source + date + URL,
   (c) concrete recommendation for TxnVigil, (d) open uncertainties.**
7. End with a single consolidated **"Decisions for TxnVigil"** table: decision · recommended option ·
   reason · source.

---

### R1. Indian regulation relevant to a fraud-analytics platform
- RBI **Master Directions on Fraud Risk Management** (2024) for commercial banks (and for NBFCs / co-operative
  banks if separate): what they require on (a) early warning signals and data analytics, (b) fraud
  classification and reporting to RBI incl. timelines, (c) role of a fraud-risk committee / CFMU, (d) staff
  accountability, (e) any requirement on use of technology/AI/ML.
- Any RBI circulars 2024–2026 on **digital payment fraud, mule accounts, transaction monitoring** (e.g.
  MuleHunter.AI by RBI Innovation Hub, Digital Payments Intelligence Platform, Central Payments Fraud
  Information Registry) — what each is, status, and what data/fields it uses.
- **DPDP Act 2023** and **DPDP Rules** (final notification date, phased commencement): obligations relevant to
  storing transaction/device data for fraud prevention (legitimate-use exemptions, retention, breach
  notification, security safeguards).
- **NPCI** UPI risk-management guidelines (transaction limits, new-device / new-beneficiary cooling limits,
  fraud-monitoring requirements for PSPs/banks), any 2024–2026 updates.
- **FIU-IND** suspicious transaction reporting basics (what triggers an STR, timelines).
- Output: compliance table → requirement · source · date · what TxnVigil should implement.

### R2. UPI / digital-payment fraud typologies in India (2024–2026)
- Latest official statistics: RBI Annual Report fraud data (latest year), I4C / NCRP cyber-fraud complaint
  numbers, NPCI fraud rates — with exact figures and URLs.
- Top typologies and how each works step by step: digital-arrest scams, investment/trading scams, task/job
  scams, fake customer-care, collect-request fraud, QR-code fraud, screen-sharing/remote-access apps,
  SIM swap, phishing/smishing, malicious APKs, mule-account networks (recruitment, renting, layering).
- For each typology: **observable signals in transaction/device/login data** a bank could use.
- Output: typology table → description · signals · data needed · recent example/news (with date & URL).

### R3. Public datasets for transaction-fraud and AML modelling
Compare at least: PaySim, BankSim, IEEE-CIS Fraud Detection, ULB Credit Card Fraud, Sparkov-generated card
dataset, IBM AMLworld (NeurIPS 2023), IBM AMLSim, SAML-D, Elliptic and Elliptic++, Amazon Fraud Dataset
Benchmark (FDB), and **any Indian/UPI dataset** if one exists.
- For each: size, time span, fraud rate, has timestamps?, has customer/account IDs?, has device/IP?,
  graph structure?, licence, download link, known issues (e.g. PaySim balance-field leakage).
- Output: comparison table + recommend the **best 2–3 to validate a UPI-style behavioural + graph model**.

### R4. State of the art in transaction fraud detection models (2022–2026)
- Is gradient boosting (LightGBM/XGBoost/CatBoost) still the strongest for tabular fraud? Cite benchmarks.
- Deep learning for tabular/sequence fraud (FT-Transformer, TabNet, TabPFN v2, sequence models over
  transaction histories, foundation models for transactions, e.g. published by Stripe/Visa/Mastercard/Nubank
  if public) — reported gains and costs.
- Handling **label delay** and **concept drift** in fraud (papers, methods, practical recipes).
- Cost-sensitive learning, calibration under class weighting, threshold selection with alert budgets.
- Unsupervised / semi-supervised detection of new fraud patterns (Isolation Forest, autoencoders) — evidence of value.
- Output: recommendation of model set for TxnVigil with justification.

### R5. Industry architecture of real-time fraud platforms
- Publicly documented architectures from: Stripe Radar, PayPal, Feedzai, FICO Falcon, Featurespace ARIC,
  NICE Actimize, SAS, Razorpay, Juspay, PhonePe, Paytm, Uber, DoorDash, Nubank, Revolut (engineering blogs,
  talks, papers).
- Typical **latency budgets**, feature-store designs, rules + ML combination, decision tiers (allow / step-up /
  hold / block), case management, feedback loops, shadow models.
- Output: reference architecture summary + list of design patterns TxnVigil should copy.

### R6. Feature store & streaming stack for laptop scale (versions as of now)
- Feast (current version, Redis online store support, on-demand features, streaming push), alternatives
  (Hopsworks, Featureform, Tecton (commercial)) — is Feast worth it vs hand-rolled Redis for this project?
- Redis data structures for sliding-window counts/sums at scale (ZSET, Redis TimeSeries, Count-Min,
  t-digest via Redis Stack) — current licence situation of Redis / Redis Stack / Valkey (2024–2026 licence changes).
- Python stream processing: Bytewax, Quix Streams, Faust (status/maintenance), plain confluent-kafka consumer.
- Redpanda vs Apache Kafka (KRaft) memory footprint and licence for local dev.
- Output: recommended stack with exact versions, licences and Docker images.

### R7. Explainability, reason codes and model governance
- SHAP TreeExplainer **inference latency** for LightGBM single-row explanations; faster alternatives
  (LightGBM `pred_contrib`, FastTreeSHAP).
- Industry practice for **reason codes** in fraud/credit decisions.
- **RBI FREE-AI framework** (2025): summary, recommendations relevant to fraud models (governance,
  explainability, monitoring, human oversight). Also any RBI/SEBI model-risk guidance.
- Model card / datasheet templates (current best versions).

### R8. Evaluation metrics used in production fraud teams
- Definitions and use of: value detection rate, account detection rate, alert-to-fraud ratio, false-positive
  ratio, precision@k / alert budget, customer friction metrics, time-to-detect.
- How banks set alert budgets; how they backtest rules; offline vs online metric gaps.
- Output: metric set + formulas TxnVigil should report.

### R9. Graph-based mule-account detection
- Methods: graph features (degree, PageRank, community, pass-through), GNNs (GraphSAGE, GAT, R-GCN,
  temporal GNNs) on AMLworld/Elliptic — reported results.
- **MuleHunter.AI** (RBIH): what is publicly known about method, features, adoption.
- Open-source tools/libraries suitable for laptop scale (NetworkX, igraph, PyTorch Geometric, DGL).
- Output: practical recipe for TxnVigil (batch graph features + optional GNN experiment).

### R10. MLOps, CI/CD and supply-chain security tooling (versions as of now)
- MLflow (latest; model registry aliases vs stages), Evidently (latest API), Prefect vs Dagster for small
  projects, DVC usefulness.
- GitHub Actions best practices 2025–2026: caching for uv/pnpm, Testcontainers in Actions, reusable workflows,
  OIDC, environments with approvals.
- Security scanning: Trivy, Grype, Syft (SBOM), gitleaks, osv-scanner, pip-audit, Semgrep, Bandit, OWASP ZAP
  baseline in CI, cosign signing — what is current and free.
- Python tooling: uv (version), ruff, mypy vs pyright; JS: pnpm, Vite, Vitest, Playwright versions.

### R11. Free or near-free hosting for the demo (2026)
- Compare: Oracle Cloud Always Free, Google Cloud free tier, AWS free tier (current terms), Fly.io, Render,
  Railway, Koyeb, Hugging Face Spaces (Docker), GitHub Codespaces — RAM/CPU limits, sleep policies, whether
  docker-compose with ~6 services is possible, India region availability, credit-card requirement.
- Output: best 2 options with exact limits and cost.

### R12. Synthetic financial data: realism and validation
- How PaySim, AMLSim, AMLworld were designed and validated.
- Methods to validate synthetic transaction data: marginal/statistical tests, TSTR/TRTS, privacy tests,
  graph-structure comparisons; libraries (SDV/SDMetrics, synthcity) current status.
- Agent-based simulation frameworks in Python suitable for this (Mesa, SimPy) — current versions.
- Output: validation checklist TxnVigil should run.

### R13. Existing open-source projects to beat
- Find the 10 most relevant open-source projects (GitHub) for real-time fraud/AML transaction monitoring
  (not only notebooks): stars, last commit date, stack, features, **main weaknesses**.
- Output: table + the 5 features TxnVigil must have to be clearly better.

---

**Final deliverable format:** one Markdown document with headings R1–R13, each with (a)–(d) as specified,
followed by the consolidated "Decisions for TxnVigil" table and a full reference list (title, author/org,
date, URL).
