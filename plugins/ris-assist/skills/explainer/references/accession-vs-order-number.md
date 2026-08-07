# Accession number vs. order number

Generic domain reference (backlog E5.1). The single most common
"why does this system show a different number than that one" question new
analysts ask.

## Depth 1 — one line

The order number identifies the *request*; the accession number identifies
the *imaging exam RIS/PACS actually performs* — they're usually assigned by
different systems, at different lifecycle stages, and are not
interchangeable even though both look like "the number for this study."

## Depth 2 — why there are two

- **Order number** — assigned when the order is created (often by the EHR
  or the ordering system), before RIS or PACS is necessarily involved at
  all. It identifies the clinical request: who ordered what, for whom.
- **Accession number** — assigned by RIS (or occasionally the modality)
  once the order becomes an imaging exam RIS needs to schedule and track.
  It identifies the *performed study* — the thing PACS stores images
  against, and the thing radiologists and PACS-side workflows reference.

One order can, depending on the site's workflow, correspond to one or more
accessioned exams — for instance a single order for "CT chest/abdomen/
pelvis" might accession as one exam or as separate accessioned studies,
depending on site configuration. That mapping is site-specific; if a user
asks how *their* site does it, that's a site-profile question, not a
generic one — say so and check `identifier_formats` / triage against the
site profile rather than guessing.

## Depth 3 — where confusing the two causes real problems

- **Searching PACS by order number** and finding nothing — PACS indexes by
  accession number. This is one of the most common "the study is missing"
  false alarms; the study exists, the wrong identifier was used to look for
  it.
- **A ticket citing "order 12345" when triaging a PACS-side symptom** — ask
  for the accession number specifically once the symptom looks PACS-side;
  the order number won't be in PACS's index at all.
- **Reconciling a report back to the originating order** — this crosses
  back from accession-space (RIS/PACS) to order-space (EHR), and is exactly
  where an outbound interface failure shows up as "report exists in RIS,
  never appeared in the chart."

When helping someone with a specific number, ask which one they have before
assuming — the two are easy to confuse precisely because both are commonly
just called "the number."
