# ADR-0002: Valkey with a hand-rolled Lua feature store over Feast and Redis

- **Status:** Accepted
- **Date:** 2026-11-02
- **Deciders:** MASTERMIND (decision), CO-MASTERMIND (record)

## Context

The scoring path reads per-customer, per-device and per-payee state (sorted-set time windows, profile
hashes, capped lists) within a few milliseconds (spec §7.3, §14.2). The same feature definitions must give
identical values online and offline (parity tests, spec §8.3). We want an open licence and as few moving
parts as possible on a laptop.

## Decision

- Use **Valkey** (BSD-3 licence, Redis-protocol compatible) as the online store, accessed with a
  **redis-py-compatible client**.
- Build a **hand-rolled feature store**: feature reads and state updates run as **atomic Lua scripts**,
  so each read or update of an entity's keys is a single server-side step.
- **Single-writer rule (spec §7.3):** only the stream-worker writes feature state; the scoring API only
  reads and computes request-time features in-process. This removes write races by construction.
- **Feast is not used.** Redis is not used in compose; a local redis-server may stand in for pure unit
  tests only (CP-0 C1).

## Consequences

### Positive

- Permissive licence with no ambiguity for a public repo.
- One network round-trip per feature read; no extra serving layer between the API and the store.
- Full control of key design, TTLs and Lua logic, which makes online/offline parity testable feature by feature.

### Negative

- **More of our own code to test:** Lua scripts, key schemas, TTL handling and the registry glue are ours.
  Bugs here are silent feature errors, so parity and property-based tests are mandatory, not optional.
- Lua scripts are a second language in the repo, with weaker tooling than Python.
- Some Redis Stack modules and newer Redis-only features are not available; we must not depend on them.
- Valkey and Redis may diverge over time; "Redis-compatible" must be re-checked if client behaviour changes.

### Follow-ups

- Parity tests: online Lua path vs offline DuckDB path on the same events (spec §8.3).
- Smoke check in compose with `valkey-cli ping` (CP-0 C1).
- Record the image tag CI pulls; no pin here.

## Alternatives considered

| Option | Why not chosen |
|---|---|
| Feast | Not needed at this scale; adds a serving layer, latency and configuration complexity (RD-1 §3). |
| Redis | Licence change makes it a worse fit for an open portfolio repo; Valkey keeps the same API (RD-1 #6, CP-0 C1). Rationale per RESEARCH.md R6 (UNVERIFIED). |

## References

- RD-1 #6 (online store), RD-1 §3 (Feast not adopted)
- CP-0 C1 (Valkey not Redis), CP-0 C6 (ADRs accepted, no version pins)
- Spec §7.3 (single writer), §7.4, §8.3, §14.2
