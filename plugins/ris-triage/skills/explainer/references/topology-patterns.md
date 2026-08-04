# RIS ↔ PACS ↔ EHR topology patterns

Generic domain reference (backlog E5.1). This is the shape of the wiring,
generically — the site profile's `systems` and `interfaces` sections are
what this site's actual topology looks like; never present this generic
pattern as if it were confirmed for a specific site.

## Depth 1 — one line

Orders usually flow EHR → RIS → modality/PACS, and results flow back the
same path in reverse — RIS is typically the hub, not EHR or PACS directly.

## Depth 2 — the common pattern

```
EHR  --order-->  RIS  --schedule/MWL-->  Modality  --images-->  PACS
EHR  <--report--  RIS  <--status---------------------------------
```

RIS is usually the system of record for the order and its status; PACS is
usually the system of record for the images; the EHR is usually where the
order originated and where the final report needs to land for the ordering
clinician to see it. An interface engine frequently sits in the middle of
every arrow above, translating and routing rather than the systems talking
directly — when a site profile lists an `interface_engine` system, assume
every arrow above actually routes through it unless the profile's
`interfaces` entries say otherwise.

## Depth 3 — where the generic pattern breaks down, and why that matters

- **Not every site routes reports back through RIS.** Some route finalized
  reports to the EHR directly from a reporting/dictation platform, bypassing
  RIS for that leg. If a "report not in EHR" ticket doesn't fit the
  RIS-to-EHR interface story, check the site profile for a separate
  reporting-platform-to-EHR interface before assuming the generic pattern
  applies.
- **PACS is not always downstream of RIS for scheduling.** Some
  configurations schedule directly against PACS or a separate worklist
  broker rather than RIS publishing to a modality worklist. This changes
  which system to check first for a "order not visible at modality" ticket.
- **Multi-site or federated PACS.** A site profile listing more than one
  PACS entry, or a PACS with HA/multi-node notes, means "PACS is down"
  needs a follow-up — down everywhere, or down for one node/site — before
  it's routable. This is exactly the kind of question the triage
  differential's "scope" field exists to capture.

Always ground a topology answer in the site profile's actual `systems` and
`interfaces` entries when they exist; use this generic pattern only when the
profile doesn't cover the specific link being asked about, and say so.
