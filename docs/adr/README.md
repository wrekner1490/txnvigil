# Architecture Decision Records

Each ADR records one decision, why it was made, and what it costs. Template: `0000-template.md`.
ADRs carry no version numbers or pins; versions live in the lockfiles and CI-pulled image tags (CP-0 C6).

| Number | Title | Status | Date |
|---|---|---|---|
| [0001](0001-redpanda-over-kafka.md) | Redpanda in dev-container mode over Apache Kafka | Accepted | 2026-11-02 |
| [0002](0002-valkey-hand-rolled-feature-store.md) | Valkey with a hand-rolled Lua feature store over Feast and Redis | Accepted | 2026-11-02 |
| [0003](0003-lightgbm-single-gbdt-family.md) | LightGBM as the single GBDT family | Accepted | 2026-11-02 |
| [0004](0004-own-jwt-rbac-over-keycloak.md) | Own JWT and server-side RBAC over Keycloak OIDC | Accepted | 2026-11-02 |
| [0005](0005-uv-ruff-pyright-toolchain.md) | uv, ruff and pyright as the Python toolchain | Accepted | 2026-11-02 |

ADR-0006 Monorepo layout — planned for P1.
