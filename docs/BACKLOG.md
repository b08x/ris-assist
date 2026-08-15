# RIS Support Plugin — Backlog

Task format: `[ ] ID (Size) — description`. Sizes: S (≤half day), M (1–3 days),
L (multi-day / needs design). Epics list the user stories they serve
(see `USER_STORIES.md`) and any external dependencies.

**Phases** (from the platform-constraint sequencing):

- **P0** — foundation & governance groundwork (parallel to everything)
- **P1** — domain explainer + comms (no approval dependencies; ships first)
- **P2** — KB pipeline (upgrades when ServiceNow MCP lands)
- **P3** — ticket clarification
- **PX** — Copilot parallel track (deferred until BAA/PHI posture confirmed)

**Message forensics is not in this backlog.** Split into a separate plugin per
[ADR-0008](adr/0008-separate-forensics-plugin.md); parked work lives in
Part 2 of [ROADMAP.md](ROADMAP.md). Former epics E3 (data hygiene) and
E9 (forensics) moved there. Epic numbers are not reused.

**External dependencies (tracked, not owned):**

- DEP-1: ServiceNow MCP access decision (scope: read incidents / write KB)
- DEP-2: M365 Copilot PHI/BAA coverage confirmation
- DEP-3: Employer/client IP + OSS publication approval

---

## E1 — Repository & Plugin Scaffold  (P0 · stories US-21, US-25, US-26)

- [ ] E1.1 (S) — Initialize public repo; Apache-2.0 license; README skeleton
      with product statement and NON-GOALS placeholder
- [ ] E1.2 (S) — Create plugin scaffold: `.claude-plugin/plugin.json`,
      `skills/`, `commands/`, `agents/`, `docs/` directories
- [ ] E1.3 (S) — Add `.claude-plugin/marketplace.json` so the repo doubles as
      its own marketplace
- [ ] E1.4 (S) — Wire `claude plugin validate` + install smoke test into CI
      (or a release checklist if CI is deferred)
- [ ] E1.5 (M) — Decide and document versioning + changelog convention
      (SemVer, keep-a-changelog)
- [ ] E1.6 (S) — Verify current Claude Desktop plugin install path against live
      docs; write adopter install instructions from a clean-machine test

## E2 — Shared Foundation: Site Profile  (P0 · stories US-22, US-23, US-04, US-09)

- [x] E2.1 (M) — Design site profile schema: systems inventory, interface
      names/directions, identifier formats, escalation matrix, SLA tiers,
      downtime procedure names, comms audiences
- [x] E2.2 (M) — Build **cold-start interview skill**: guided first-run
      interview → writes profile to a local path outside the plugin cache
- [ ] E2.3 (S) — Build **customize skill**: single-field profile edits without
      re-interview
- [x] E2.4 (S) — Define graceful-degradation convention: how every skill
      behaves when a profile field is missing (state the gap; never improvise)
- [x] E2.5 (S) — Author the fictional example site profile ("worked example"
      demonstrating the schema) for `examples/`

## E4 — Persona & Agent Definition  (P0 · stories US-01…US-19 cross-cutting)

- [x] E4.1 (M) — Author persona spec: stance, observation/inference separation,
      confidence marking (confirmed/likely/possible), cite-or-decline rule,
      audience register shifting, human-decision boundaries
- [x] E4.2 (S) — Encode persona as `agents/` subagent definition
- [x] E4.3 (S) — Embed persona behavioral rules into each skill's instructions
      (Desktop-chat path) — single source file, referenced not duplicated
- [ ] E4.4 (S) — Promote boundary rules to `docs/NON-GOALS.md` (US-27)

## E5 — Domain Explainer Skill  (P1 · stories US-07, US-20)

- [x] E5.1 (M) — Author reference docs: order lifecycle, accession vs. order
      number, MWL, report status flow, RIS↔PACS↔EHR topology patterns
- [x] E5.2 (S) — Build explainer skill: depth-adjustable answers; site-specific
      claims grounded in profile; generic claims grounded in reference docs
- [x] E5.3 (M) — Build onboarding path: sequenced explainer curriculum for a
      new analyst (US-20)
- [ ] E5.4 (S) — Validation pass: use explainer to stress-test topology schema
      accuracy (cheap end-to-end test of E2)

## E6 — Communications Skill  (P1 · stories US-15…US-19)

- [ ] E6.1 (M) — Author template library: downtime (planned/unplanned/degraded/
      resolved) × audience (clinical/IT/leadership); MIM cadence set (initial/
      interval/all-clear); vendor ticket forms; change narrative; PIR skeleton;
      shift-turnover format
- [ ] E6.2 (S) — Build comms skill: template selection + slot-filling; unknown
      required fields marked, never invented
- [ ] E6.3 (S) — `/downtime` slash command
- [ ] E6.4 (S) — MIM continuity behavior: interval updates carry prior facts,
      prompt only for the delta (US-16)

## E7 — KB Pipeline  (P2 · stories US-11…US-14 · DEP-1)

- [x] E7.1 (M) — Adapt existing ServiceNow KB generator skill into the plugin:
      triage-first HTML article shape, import formatting rules, and the
      HTML → DOCX renderer. Supersedes the KCS markdown template that shipped
      in 1.0.0 — see ADR-0009
- [x] E7.2 (S) — Manual-mode path: article draft as a Word-openable HTML file
      plus outstanding items and field checklist (works with zero ServiceNow
      access and zero installed tooling — ADR-0010)
- [ ] E7.3 (M) — MCP-mode path: read resolved incident → draft → push with
      category/workflow state  *(blocked: DEP-1)*
- [ ] E7.4 (M) — KB gap detection: recurring-symptom clusters without matching
      articles → candidate list (US-12) *(needs incident read: DEP-1 — manual-
      mode partial: skill now prompts explicitly when a pattern is described)*
- [x] E7.5 (S) — Stale-article flagger keyed to change/upgrade events (US-13)
- [x] E7.6 (S) — `/draft-kb` slash command (`Bash` allowed for the render step
      only)

## E8 — Ticket Clarification Skill  (P3 · stories US-03…US-06)

- [x] E8.1 (M) — Design differential model (RIS config / interface / PACS /
      workstation / user) + discriminating-question selection logic
- [x] E8.2 (M) — Build clarification skill: one-question-at-a-time elicitation;
      stop condition = routable
- [x] E8.3 (S) — Triage artifact output format: symptom, scope, timeline,
      differential w/ confidence, recommended queue
- [x] E8.4 (S) — Routing + severity justification against site SLA vocabulary
      (US-04)
- [x] E8.5 (M) — Escalation package assembler (US-05)
- [ ] E8.6 (S) — `/troubleshoot` slash command
- [x] E8.7 (M) — Known-error matching against KB *(blocked: DEP-1 for live;
      manual paste-mode works without)*

## E10 — Governance & Approvals  (P0, longest lead time · US-28, US-29)

- [ ] E10.1 (S) — Draft publication approval note: exactly what is public,
      the private/public boundary, fictional example attached *(feeds DEP-3)*
- [ ] E10.2 (S) — Submit and track DEP-3 (employer/client IP + OSS sign-off)
- [ ] E10.3 (S) — Request DEP-2 determination (Copilot PHI/BAA posture) —
      outcome decides the PX track
- [ ] E10.4 (S) — Track DEP-1 (ServiceNow MCP scope decision); document
      granted scopes in `docs/`
- [ ] E10.5 (S) — Scrub check: pre-publication review that no client, MSP, or
      site-identifying detail exists anywhere in repo or history

## E11 — Transparency & Publishing  (continuous · US-25, US-26)

- [ ] E11.1 (S) — ADR framework in `docs/adr/`; backfill ADRs for decisions
      already made (symbolic-first parsing, platform split, cold-start
      pattern, synthetic-only data, Apache-2.0)
- [ ] E11.2 (S) — AI-assisted development disclosure in README: what was
      co-developed, how outputs are validated
- [ ] E11.3 (S) — Commit hygiene convention: real history, no squash-dumps
- [ ] E11.4 (S) — `docs/NON-GOALS.md` published (from E4.4)
- [ ] E11.5 (M) — Reader-test pass: fresh-context review of README + docs;
      fix what a cold reader gets wrong
- [ ] E11.6 (S) — Demo the onboarding skill's `interview` mode: the write-path
      question, "we don't distinguish that" recorded as absence, the overnight
      audience second pass, and the pasted-inventory branch (currently the only
      demonstrable instance of symbolic-parse-before-interpretation, since the
      HL7 parser is gated behind ADR-0008). Proves question sequence and
      refusal behavior only — elicitation is not scriptable; label it as such.
      Blocked on nothing; `review` mode is all any demo covers today.

## E12 — Copilot Parallel Track  (PX · deferred until DEP-2 resolves)

- [ ] E12.1 (M) — Port capability instructions + reference docs to SharePoint
      knowledge-source format (same source markdown, different mount)
- [ ] E12.2 (L) — Copilot Studio agent for live-ticket clarification
- [ ] E12.3 (L) — Power Automate flow: envelope extraction + segment split
      pre-parse for live messages (symbolic layer, Copilot idiom)
- [ ] E12.4 (S) — Decision record: what runs where and why, by data
      sensitivity (publishable as an ADR)

---

## Suggested first sprint (if starting Monday)

E1.1–E1.3, E2.1, E4.1, E10.1–E10.3 — scaffold exists, schema drafted,
persona specified, and all three long-lead
approval clocks started. Everything else stacks behind those.

---

## Addendum — E6 revision (comms customization)

`/downtime` cannot ship on a fixed template set; notification practice varies
too much between sites and audiences. E6 is revised to make the profile the
product and the templates the fallback.

- [x] E6.5 (M) — Define comms profile schema: variants keyed by
      `event class × audience × channel`, plus conventions, distribution,
      approval chain, workflow language, cadence, voice rules, and a recorded
      `gaps` list
- [ ] E6.6 (M) — Build `/comms-config` **capture** mode: infer variants from
      pasted example notifications; show extraction for confirmation before
      writing; warn once about local storage of staff names/contacts
- [ ] E6.7 (M) — Build **build** mode: one-question-at-a-time interview,
      derived as deltas from the site's most common notification
- [ ] E6.8 (S) — Build **edit** mode: single-variant change, no re-interview,
      other entries preserved
- [ ] E6.9 (S) — Build **review** mode: coverage against axes, gaps ranked by
      likely need, no auto-fill
- [ ] E6.10 (S) — Nearest-variant substitution behavior in `/downtime`, with
      the substitution stated in the output
- [ ] E6.11 (S) — Incident continuity: interval updates and all-clears carry
      forward reference, start time, and prior impact; changed facts flagged
      as changed
- [x] E6.12 (S) — Author `references/generic-templates.md` fallbacks, labelled
      untuned in output
- [x] E6.13 (S) — Author `references/register-guide.md` — clinical vs.
      technical vs. leadership register, with worked examples
- [x] E6.14 (S) — `/uptime` slash command: resolution-side counterpart to
      `/downtime` (same comms skill, same profile, same continuity rules),
      scoped to the moment a service comes back rather than the moment it
      goes down

Stories served: US-15, US-16, US-17, US-23. New story implied — *as a support
lead, I want to teach the plugin how my site writes notifications, so drafts
arrive in our voice rather than a generic one* (add as US-30).
