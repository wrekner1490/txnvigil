# ADR-0001: Redpanda in dev-container mode over Apache Kafka

- **Status:** Accepted
- **Date:** 2026-11-02
- **Deciders:** MASTERMIND (decision), CO-MASTERMIND (record)

## Context

TxnVigil needs an event log between the scoring API, the stream-worker, the parquet sink and the
analyst UI (topics in spec §13.3). The whole core stack must run on one laptop inside a tight memory
budget (RD-1 #6d: six core containers, target total memory under load stated there). The broker must speak
the Kafka protocol so that standard Kafka clients and skills apply.

## Decision

- Use **Redpanda** as the broker, run in **dev-container mode**: a single core (`--smp 1`) and an
  explicit memory cap, plus a compose `mem_limit`.
- Consume with **plain `confluent-kafka` consumers** written in our own code.
- Do **not** use a stream-processing framework: no Bytewax, no Faust, no Flink.
- Code talks only to the Kafka API, never to Redpanda-specific APIs, so the broker stays swappable.

## Consequences

### Positive

- One binary, no separate controller or ZooKeeper process; fast start-up in compose and in CI.
- Lower memory footprint fits the laptop budget, per RESEARCH.md R6 (UNVERIFIED).
- Plain consumers are simple to read, unit-test and reason about (offsets, retries, idempotency are explicit).

### Negative

- **Licence:** Redpanda's community edition is published under the Business Source License (BSL), not an
  OSI-approved open-source licence. We have not made any legal assessment; whether BSL terms suit a
  public portfolio repo and a free hosted demo must be checked against the licence text before P7.
- Windowing, joins and exactly-once semantics that a framework would give us must be built and tested by hand.
- Dev-container mode is not a production configuration; any production-readiness claim must say so.
- Some Kafka operational tooling and behaviours differ slightly between Redpanda and Apache Kafka.

### Follow-ups

- Record the image tag CI actually pulls (RD-1 §0); no pin in this ADR.
- Licence check of the Redpanda image before the public release (P7); record the result in docs.
- Integration tests run against the real broker via Testcontainers in CI.

## Alternatives considered

| Option | Why not chosen |
|---|---|
| Apache Kafka (KRaft mode) | Fully open licence, but heavier on JVM memory and start-up time for a laptop stack. Remains the fallback: Kafka-API-only code makes the swap cheap. |
| Bytewax / Faust / Flink | Extra runtime and learning surface for logic that plain consumers handle at this scale (RD-1 #6b). |

## References

- RD-1 #6b (broker and consumer), RD-1 #6d (compose core profile), RD-1 §0 (versions)
- CP-0 C6 (ADRs accepted, no version pins)
- Spec §7.4 (technology choices), §13.3 (topics)
