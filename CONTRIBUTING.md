# Contributing

Adopters at other sites are the audience this is designed for.

## Before anything else

**Never open a pull request containing real clinical data.** Not raw, not
scrubbed, not de-identified, not "based on" a real message with the names
changed. Such PRs are closed without merge. See
[docs/DATA-PROVENANCE.md](docs/DATA-PROVENANCE.md) for why de-identification is
not sufficient.

The same applies to real site detail: interface names, distribution lists,
staff names, form numbers, phone extensions, organization names. If it
identifies a real site, it does not belong here.

## Useful contributions, roughly in order of value

1. **Site profile schema gaps** — a field your environment needs that the
   cold-start interview does not ask about. These are the highest-value reports
   because they are exactly what a single-site author cannot see.
2. **Audience and register gaps** — a role you notify that the default set does
   not cover, or a register rule that does not hold at your site.
3. **Reference corrections** — anything factually wrong about HL7, KCS, or
   radiology workflow.
4. **Fictional test cases** — realistic failure modes, invented data only.

## Design constraints a PR should respect

- Deterministic where it can be. If code can decide it, code decides it.
- Gaps render explicitly. An empty result that reads as "fine" is a defect.
- Observation is separated from inference; conclusions carry a confidence mark.
- Nothing executes. The plugin drafts and recommends.
- Site specifics live in the local profile, never in this repository.

Full statement: [docs/NON-GOALS.md](docs/NON-GOALS.md).

## Decisions

Substantive design changes get an ADR in [docs/adr/](docs/adr/), including the
alternatives rejected. If your PR changes how something works rather than what
it says, include one.

## AI-assisted contributions

Welcome, and worth disclosing in the PR description — that is the norm this
project is trying to set, not a hurdle.
[docs/GUARDRAILS.md](docs/GUARDRAILS.md) documents the failure modes this
project checks its own AI-assisted work against; they are a reasonable
checklist for contributions too.
