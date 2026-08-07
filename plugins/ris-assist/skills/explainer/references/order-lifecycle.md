# Order lifecycle

Generic domain reference (backlog E5.1). Site-specific system names come
from the site profile, not from here — if you're answering a user, cite
which parts of this you're grounding generically vs. from their profile.

## Depth 1 — one line

An imaging order moves from *ordered* to *scheduled* to *performed* to
*read* to *reported*, and each stage has a status that other systems key
off of.

## Depth 2 — the stages

1. **Ordered.** A referring provider (or the EHR on their behalf) creates an
   order. This is where the order number is assigned.
2. **Received.** RIS receives the order — either entered directly or via an
   interface from the EHR (see `topology-patterns.md`). This is typically
   where the accession number is assigned, distinct from the order number
   (see `accession-vs-order-number.md`).
3. **Scheduled.** The order is matched to a modality, room, and time slot.
   Scheduling failures here are a common "order exists but nobody can find
   it" symptom.
4. **Published to modality worklist.** The scheduled order becomes visible
   to the imaging modality as a worklist entry (see `modality-worklist.md`)
   — this is the step a broken RIS-to-PACS/modality interface most visibly
   breaks.
5. **Performed.** The technologist executes the study; images are acquired
   and sent to PACS. Order status updates to reflect this.
6. **Read.** A radiologist reads the study, typically via PACS, sometimes
   using a dictation platform.
7. **Reported.** The report is finalized and released — usually back
   through RIS, and often back out to the EHR the order originated from.

## Depth 3 — where it breaks, and what that looks like

- **Order stuck at "received," never scheduled.** Usually a scheduling rule
  or a missing modality/resource mapping — not typically an interface
  problem.
- **Order scheduled but never reaches the modality worklist.** Classic
  interface symptom — the RIS-to-PACS (or RIS-to-modality) interface is
  down or queuing. This is the single most common overnight ticket shape.
- **Study performed but report never appears in the EHR.** Look at the
  far end of the pipeline — report release from RIS, or the outbound
  interface back to the EHR — not the imaging side.
- **Order exists in EHR, not in RIS at all.** The inbound order interface
  (EHR-to-RIS) is the first thing to check, before assuming a RIS
  configuration problem.

Each of these maps onto a differential branch in the `triage` skill —
this document is what a triage differential's "RIS configuration vs.
interface vs. PACS" branching is actually reasoning about.
