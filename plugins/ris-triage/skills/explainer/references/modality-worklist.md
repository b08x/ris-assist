# Modality worklist (MWL)

Generic domain reference (backlog E5.1).

## Depth 1 — one line

The modality worklist is the list a scanner or other imaging device queries
to find out what it's supposed to be scanning next — if an order isn't on
it, the technologist can't select it at the machine.

## Depth 2 — how it works

RIS (or the interface engine on RIS's behalf) publishes scheduled orders to
a worklist the modality queries — typically the modality asks "what's
scheduled for me, right now" and gets back a list of pending exams with
patient/order/accession identifiers attached. The technologist selects the
correct entry at the console rather than typing patient details by hand,
which is the whole point: MWL is what keeps images acquired at the modality
correctly tagged with the right patient and accession number.

## Depth 3 — failure modes

- **Order scheduled in RIS, not appearing at the modality.** The interface
  between RIS and the modality (often via the interface engine) is down,
  queuing, or filtering the order out — this is the textbook "RIS-to-PACS
  order interface" failure named throughout this plugin's examples. Check
  whether *other* orders are reaching the same modality — if none are,
  it's the interface or the modality's worklist query itself; if only one
  order is missing, look at that order's status in RIS first.
- **Worklist entry present but wrong/stale patient data.** Usually a sign
  the ADT (patient demographics) feed is stale or the order was scheduled
  before a late demographic correction — different root cause than a
  missing entry, even though both look like "MWL is wrong" to the
  reporting technologist.
- **Technologist scans without selecting from worklist ("manual entry").**
  Produces an exam not properly linked to the original order/accession —
  a common downstream cause of "study performed, doesn't match the order"
  tickets, and worth asking about directly when an order/exam mismatch is
  reported with no interface symptoms.

Ask which of these three shapes the ticket resembles before assuming an
interface is down — only the first one actually is.
