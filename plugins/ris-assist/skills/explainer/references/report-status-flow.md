# Report status flow

Generic domain reference (backlog E5.1).

## Depth 1 — one line

A report moves through a small set of statuses — roughly *dictated* →
*transcribed/draft* → *finalized* → *released* — and "where is my report"
tickets almost always mean the report is stuck at one specific stage, not
missing entirely.

## Depth 2 — the stages

1. **Dictated.** Radiologist dictates findings, via a dictation platform or
   directly in RIS/PACS. Nothing is visible outside RIS yet.
2. **Transcribed / draft.** Speech becomes text — automatically (speech
   recognition) or via a transcription step. Status is typically something
   like "preliminary" or "draft" — visible in RIS, not yet authoritative.
3. **Finalized / signed.** The radiologist reviews and signs the report.
   This is the point the report becomes the official record.
4. **Released / distributed.** The finalized report is sent onward — back
   to the ordering EHR, to referring providers, sometimes to a patient
   portal. This is a separate step from finalization and has its own
   failure modes.

## Depth 3 — where "where's my report" tickets actually point

- **Stuck at dictated/draft, no finalized report.** Look at the radiologist
  workflow side — pending signature queue, dictation platform issue — not
  at an interface. This is not a RIS-to-EHR problem yet.
- **Finalized in RIS, never appears in the EHR.** This is an outbound
  interface problem — the report-release interface, distinct from the
  inbound order interface. Confirm the report shows "released" status in
  RIS before escalating the interface, since a report that's merely
  finalized-not-released will look identical to the referring provider
  either way.
- **Released, but to the wrong recipient or none.** Usually a routing rule
  or distribution configuration issue tied to how the original order
  specified the ordering provider — check whether the order's referring-
  provider field was populated correctly, which traces back to the order
  lifecycle's "ordered" stage, not to anything report-side.

The useful triage question is almost always "what status does RIS show for
this report" before anything else — the answer usually narrows which of
the three failure shapes above applies immediately.
