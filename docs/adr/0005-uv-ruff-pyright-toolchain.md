# ADR-0005: uv, ruff and pyright as the Python toolchain

- **Status:** Accepted
- **Date:** 2026-11-02
- **Deciders:** MASTERMIND (decision), CO-MASTERMIND (record)

## Context

The Python side needs reproducible dependency resolution, linting, formatting and static type checking
that run quickly in CI and in the cloud workspace. Exact versions must come from what actually installs,
not from the research report (RD-1 §0).

## Decision

- **uv** for packaging, virtual environments and the lockfile.
- **ruff** for both linting and formatting (one tool, one config in `pyproject.toml`).
- **pyright** for type checking, **strict on `core/`**; it **replaces mypy** (CP-0 C2).
- **The lockfile is the version source of truth (RD-1 §0).** `pyproject.toml` declares lower bounds only;
  a CI `lock` job runs `uv lock` and uploads the lockfile as an artefact; the user commits it, after which
  CI installs with `uv sync --frozen` (CP-0 K2).
- `requires-python` and the CI interpreter matrix follow CP-0 C4: two Python versions are tested during
  P0–P1, and one is chosen at CP-1. This ADR does not name them.

## Consequences

### Positive

- Fast installs and checks; short CI feedback loops.
- Fewer tools to configure (ruff covers what several linters and a formatter did).
- Strict typing on the shared library catches contract errors between services early.

### Negative

- pyright is a Node-based tool; CI and the workspace need it available, and its strict mode may
  disagree with libraries that ship weak type stubs, needing targeted ignores.
- The lockfile must be generated in CI first (registries are blocked in the cloud workspace, per CP-0 T00),
  so early tasks run without a committed lock.
- uv and ruff move fast; behaviour changes arrive through lockfile updates and must be reviewed.

### Follow-ups

- CI jobs: `ruff check`, `ruff format --check`, `pyright`, `lock`, plus the non-blocking deps-probe (CP-0 C4).
- Pick one Python version at CP-1 and update the matrix.
- JS side (pnpm, Vite, Vitest, Playwright) follows the same lockfile rule; recorded in the spec, not here.

## Alternatives considered

| Option | Why not chosen |
|---|---|
| mypy | Replaced by pyright for speed and stricter inference (CP-0 C2). |
| poetry / pip-tools | Slower resolution and more tooling for the same outcome (spec §7.4). |
| black + flake8 + isort | Three tools where ruff covers all three. |

Rationale wording per RESEARCH.md R10 (UNVERIFIED).

## References

- RD-1 #10 (tooling), RD-1 §0 (versions from lockfile)
- CP-0 C2 (pyright replaces mypy), C4 (Python matrix), K2 (lockfile flow), C6 (no version pins)
- Spec §7.4, §17.1
