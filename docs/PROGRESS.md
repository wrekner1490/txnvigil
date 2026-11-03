# TxnVigil v2 — Progress

Last updated: 2026-11-02

**Current phase: P0 — Foundations** (plan approved at CP-0, see [DECISIONS.md](DECISIONS.md)).

## Phase overview

| Phase | Name | Status | Plan checkpoint |
|---|---|---|---|
| P0 | Foundations | IN PROGRESS | CP-0 APPROVED WITH REQUIRED CHANGES |
| P1 | Data | TODO | — |
| P2 | Features | TODO | — |
| P3 | Models | TODO | — |
| P4 | Serving | TODO | — |
| P5 | Ops UI | TODO | — |
| P6 | MLOps | TODO | — |
| P7 | Ship | TODO | — |

## P0 tasks

Deliveries per CP-0 D-F: DLV-1 = T01 + T02 + T06, DLV-2 = T03 + T04, DLV-3 = T05.

| ID | Title | Status | Owner | Delivery | Commit/PR | Date |
|---|---|---|---|---|---|---|
| P0-T00 | Environment probe | DONE | WORKER | — | — | 2026-11-02 |
| P0-T01 | Repo bootstrap + v1 move to legacy/v1/ | IN DELIVERY | WORKER | DLV-1 | | 2026-11-02 |
| P0-T02 | Spec update (D-D + D5 + FR-13a + RD-1) | IN DELIVERY | WORKER | DLV-1 | | 2026-11-02 |
| P0-T06 | ADRs 0001–0005 | IN DELIVERY | WORKER | DLV-1 | | 2026-11-02 |
| P0-T03 | Monorepo skeleton | TODO | WORKER | DLV-2 | | |
| P0-T04 | CI skeleton | TODO | WORKER | DLV-2 | | |
| P0-T05 | Compose core (Valkey / Redpanda / Postgres) | TODO | WORKER | DLV-3 | | |

Status values: TODO → IN PROGRESS → IN DELIVERY (files prepared, awaiting user commit + CI) → DONE
(CI green and "MERGE OK", CP-0a D2).

## Approved cut order (CP-0 9b)

If behind schedule, cut in this order:

1. COULD items
2. Isolation Forest
3. OpenTelemetry
4. Stress + soak perf
5. Evidently (PSI script stays)
6. Champion–challenger (manual promote stays)
7. Models page
8. Policy what-if page (API stays)
9. Second public dataset

Never cut past the D5 scope floor (CP-0a D5) → slip and escalate instead.
