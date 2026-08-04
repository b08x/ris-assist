# ADR-0008 — Separate message forensics into its own plugin

Status:   Accepted
Date:     2026-08-04

## Context

The plugin was scoped with five capabilities: message forensics, ticket
clarification, knowledge capture, communications, and domain explanation. Four
of them are ready to build. Forensics is not, for three independent reasons.

**Access.** Forensics needs message data to develop against and to validate.
That access has not been granted, and the request is not in flight yet. Every
other capability can be built and demonstrated without it.

**Critical path contamination.** Two P0 epics existed almost entirely to serve
forensics: the synthetic HL7 corpus generator and the de-identification gate
(E3). Both were gating phase 0 alongside genuinely shared work — the repository
scaffold, the site profile, the persona — despite no other capability depending
on them. The core plugin was waiting on infrastructure it does not use.

**Demonstrability.** Under G8, a capability cannot be demoed before its
supporting mechanism exists. Forensics without the symbolic parse layer is
exactly the model-freestyle-parsing behavior this project was created to argue
against. Keeping it in the core scope creates continuous pressure to demo it
anyway, since it is the most impressive of the five.

## Decision

Split forensics into a second plugin, `ris-triage-forensics`, published from the
same repository and listed in the same `marketplace.json`.

Moves to the forensics plugin: E3 (synthetic corpus, de-identification gate) and
E9 (forensics skill), plus the GBNF grammar work as a new deferred item.

Stays in the core plugin: clarification, knowledge capture, communications,
domain explanation, the site profile machinery, the persona, and all governance
and transparency work.

Forensics is deferred to a long-term backlog with no phase assignment. It is not
scheduled; it is parked with its dependencies stated.

## Alternatives considered

**Keep it in one plugin, deprioritized.** Rejected. A capability listed in the
README as unbuilt still shapes expectations, still attracts demo pressure, and
still leaves its infrastructure sitting in phase 0. Deprioritizing inside one
scope is a statement of intent; splitting is a structural change.

**Separate repository.** Rejected. It would fragment the ADR record, the commit
history, and the transparency argument across two places for no gain. A
marketplace registry can list multiple plugins from one repository, so adopters
still install them independently — which was the only real benefit of separate
repos.

**Build forensics first, since it is the hardest.** Rejected. It has the
strongest external dependency and the weakest current substrate. Building the
four unblocked capabilities produces something usable while access is pending,
and produces the site profile that forensics will need anyway.

## Consequences

**Easier:** the core plugin's phase 0 shrinks to work that actually serves it.
Nothing in the initial release waits on a data access decision. The
demonstrability line is structural rather than a matter of discipline.

**Harder:** the de-identification gate now lives in the forensics plugin, so if
any core capability later needs to ingest raw messages, that dependency has to
be reconsidered — likely by promoting the gate to a shared component. Noted as a
known future decision rather than solved now.

**Committed to:** a multi-plugin marketplace layout from the start, which means
the scaffold work in E1 has to accommodate two plugin directories even though
only one is being built. Cheaper now than retrofitting.

**Documentation:** `docs/NON-GOALS.md` gains a line stating that message
forensics is deliberately a separate plugin and why, so its absence reads as a
decision rather than an omission.
