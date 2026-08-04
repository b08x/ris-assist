# RIS Triage Forensics — long-term backlog

Parked, not scheduled. Split out of the core plugin per
[ADR-0008](adr/0008-separate-forensics-plugin.md).

Nothing here has a phase. This backlog is a record of what the work is and what
it waits on, so the shape of it isn't rediscovered later.

## Blocking dependencies

| | Dependency | Status |
|---|---|---|
| **F-DEP-1** | Access to message data for development and validation | Not requested |
| **F-DEP-2** | Site profile schema stable enough to encode interface topology | Follows core E2 |
| **F-DEP-3** | Local model evaluation, if grammar-constrained generation is pursued | Not started |

F-DEP-1 is the real gate. Everything else can proceed once it clears.

---

## FE1 — Data hygiene (was core E3)

Moved wholesale. These existed to serve forensics and were gating core phase 0
for no reason.

- [ ] FE1.1 (M) — Synthetic HL7 v2 message generator (ORM/ORU/ADT/SIU;
      fictional patients; structurally valid; seedable)
- [ ] FE1.2 (S) — Generate and commit the reference corpus, including
      deliberately malformed messages for negative tests
- [ ] FE1.3 (M) — Deterministic de-identification gate: PID/NK1/IN1/GT1
      scrub/synthesize pass, plus a free-text (OBX/NTE) second pass
- [ ] FE1.4 (S) — Test suite: de-id gate against the synthetic corpus,
      including PHI planted in free text
- [ ] FE1.5 (S) — Data provenance statement specific to this plugin

Note: `docs/DATA-PROVENANCE.md` already states the synthetic-from-birth policy
for the core plugin. When FE1 is built, that document either extends to cover
both or forks — decide then.

## FE2 — Symbolic parse layer (was core E9.1–E9.2)

The whole argument rests on this existing before any model interpretation.

- [ ] FE2.1 (L) — Parser: envelope extraction, segment splitting, field mapping
      into a structured representation. Code, not model.
- [ ] FE2.2 (M) — Reference tables: segment/field definitions for ORM/ORU/ADT/
      SIU; common ACK error codes; Z-segments handled as declare-unknown
- [ ] FE2.3 (S) — Decide build-vs-adopt: an existing HL7 library (hl7apy, HAPI)
      versus a purpose-built parser. Adopting is likely correct; record the
      decision as an ADR either way.

## FE3 — Diagnosis layer (was core E9.3–E9.6)

- [ ] FE3.1 (M) — Diagnosis instructions: reason over parsed structure, apply
      confidence marking, hypothesize fault origin from site topology
- [ ] FE3.2 (M) — Message diff with expected-variance suppression
      (timestamps, control IDs) separated from structural difference
- [ ] FE3.3 (M) — Blast-radius analysis from the topology graph
- [ ] FE3.4 (M) — Replay-safety advisory, with hard human-authorization flag on
      any sequence-sensitive case (ADT merges, cancels)
- [ ] FE3.5 (S) — `/decode` command
- [ ] FE3.6 (M) — Evaluation set: known-fault synthetic messages with expected
      findings, run as regression

## FE4 — Grammar-constrained generation (new, speculative)

Investigated 2026-08-04. Worth recording, not worth committing to.

GBNF constrains *generation*, not parsing — it will not parse inbound messages,
so it has no role in FE2. Two places it could earn its keep:

- [ ] FE4.1 (S) — **Spike first.** Test whether a local model holds up under
      HL7-shaped constrained decoding at all. Heavily delimited output with long
      fields is a regime where constrained sampling sometimes degrades badly.
      An hour with a generic-tier grammar answers it. Everything below is
      contingent on this.
- [ ] FE4.2 (M) — Generic structural grammar: MSH with hardcoded encoding
      characters, segment/field/repetition/component/subcomponent hierarchy,
      escape sequences, `\r` terminator
- [ ] FE4.3 (M) — Message-type overlays constraining segment order and
      cardinality for the two or three types forensics actually reasons about.
      Do not attempt field-by-field coverage of a full ORM — that is weeks of
      work for test fixtures that need representative structure, not exhaustive
      conformance.
- [ ] FE4.4 (M) — Semantic validator for what a context-free grammar cannot
      express: message type agreeing with segments present, order numbers
      matching across ORC/OBR, values drawn from HL7 tables, conditional
      requiredness by trigger event, timestamp ordering
- [ ] FE4.5 (S) — Mutation harness for malformed cases. A strict grammar cannot
      emit invalid messages; generate valid then mutate, keeping a labelled
      expected-failure per case (feeds FE3.6).
- [ ] FE4.6 (S) — Consider GBNF for constraining *forensic output* to a schema
      with mandatory confidence marking — arguably a better use than HL7 itself,
      since it makes the marking structurally unskippable rather than
      instruction-dependent.

Applies only to local model pipelines (llama.cpp and derivatives). The Anthropic
API does not accept GBNF.

The provenance argument is the strongest reason to do this at all: "generated
from a published grammar" is more defensible to a compliance reviewer than
"generated from a script."

## FE5 — Packaging

- [ ] FE5.1 (S) — Second plugin directory and `marketplace.json` entry
- [ ] FE5.2 (S) — README stating the access dependency plainly, and that the
      plugin does not ship until the parse layer exists
- [ ] FE5.3 (S) — Decide whether the de-identification gate stays here or is
      promoted to a shared component (flagged as a future decision in ADR-0008)

---

## What is deliberately not here

SFL-based analysis. The forensic *narrative* — how a finding gets written up —
may benefit from register and modality analysis, but that belongs with the
clarification work in the core plugin. HL7 messages are not natural language;
segment parsing is a formal grammar problem, and applying systemic functional
linguistics to it would be forcing the frame.
