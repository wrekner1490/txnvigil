# ADR-0004: Own JWT and server-side RBAC over Keycloak OIDC

- **Status:** Accepted
- **Date:** 2026-11-02
- **Deciders:** MASTERMIND (decision), CO-MASTERMIND (record)

## Context

The case-service and analyst UI need authentication and role-based authorisation for five roles
(analyst, risk_manager, model_risk, admin, compliance), with every login, case view and export audited
(spec §20, FR-16). Case-service JWT/RBAC/audit is in the scope floor (D5); Keycloak is a COULD item.
The core compose stack must stay small enough for a laptop.

## Decision

- Implement **our own JWT authentication**: short-lived access tokens plus refresh tokens,
  passwords hashed with **Argon2id**, lockout after repeated failures.
- **RBAC is enforced server-side** in API dependencies; the UI hides controls but is never the guard.
- Auth events (login, failure, lockout) go to the hash-chained audit log.
- **Keycloak OIDC stays COULD**; the auth layer is kept behind a small interface so OIDC can be added later.

## Consequences

### Positive

- No extra container or realm configuration in the core profile; fast tests and simple local setup.
- Roles and permissions live next to the code that needs them and are easy to unit-test.
- Clear, demonstrable security code for reviewers.

### Negative

- **Security responsibility is ours:** token signing and key handling, expiry, refresh rotation and
  revocation, lockout and timing-safe comparison must be implemented and tested correctly. A mistake here
  is a real vulnerability, not a missing feature.
- No SSO, MFA or federation out of the box.
- Hand-rolled auth needs its own security tests (authz matrix per role, expired/forged token cases).

### Follow-ups

- Use maintained libraries for JWT handling and Argon2id; do not implement crypto primitives ourselves.
- Role-by-endpoint authorisation tests; negative tests for forged, expired and wrong-audience tokens.
- Signing key from environment only, never committed (spec §16.5).
- Revisit Keycloak if the cut order (CP-0 9b) leaves time.

## Alternatives considered

| Option | Why not chosen |
|---|---|
| Keycloak OIDC | Mature and feature-rich, but adds a heavy container and configuration to the core stack; kept as COULD (D5). |
| Managed identity provider | Needs a cloud account and network; out of scope until hosting (P7). |

## References

- Spec §20 (security), §7.6, §16.5
- D5 (scope floor: JWT/RBAC/audit MUST, Keycloak COULD)
- CP-0 C6 (ADRs accepted, no version pins)
