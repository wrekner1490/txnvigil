# TxnVigil v2 — Real-Time Transaction Risk & Mule-Detection Platform

> **Status: v2 in progress — Phase P0 (Foundations).** Nothing is built or measured yet.
> This README makes **no metric or result claims**; numbers will appear only once the
> repository itself produces them.

> **Data:** synthetic and public data only. No real bank data, no real customer data, no PII.

## Vision

An open, explainable, real-time platform that scores every UPI-style payment, detects mule networks,
routes risky payments to tiered actions, and gives analysts a case workflow whose decisions feed back
into the model. The goal is to measure, on more than one dataset, whether it does better than rules
alone (spec §3).

## Where to look

- Build specification: [docs/TXNVIGIL_BUILD_SPEC.md](docs/TXNVIGIL_BUILD_SPEC.md)
- Progress and task status: [docs/PROGRESS.md](docs/PROGRESS.md)
- Decision log: [docs/DECISIONS.md](docs/DECISIONS.md)
- Requirement traceability: [docs/traceability.csv](docs/traceability.csv)

## Development (P0)

Prerequisites: [uv](https://docs.astral.sh/uv/) and Python ≥ 3.12.

```sh
make sync   # create .venv with the dev tools (uv sync --group dev)
make lint   # ruff check, ruff format --check, pyright (strict on core/)
make test   # pytest with coverage (gate: 80% on core/)
```

`make help` lists all targets. CI is the authoritative test runner; local runs are a pre-check.

## v1

v1 (frozen, not maintained) lives in [legacy/v1/](legacy/v1/). Its results are v1-only and synthetic
and do not describe v2. See [legacy/README.md](legacy/README.md).
