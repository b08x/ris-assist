# Integration Standards Reference

Generic domain reference. This covers the standards that connect RIS, PACS,
EHR, and modalities — not any site's specific configuration of them.

## Depth 1 — one line

Radiology systems communicate via HL7v2 (clinical data: orders, results,
demographics) and DICOM (imaging data: worklist, images, status) — these
are different standards for different data types, bridged by the RIS or
middleware.

## Depth 2 — the standards landscape

### HL7v2 (Health Level Seven Version 2.x)

The messaging standard for clinical data exchange. Pipe-delimited, segment-
based, with trigger events driving message flow.

**Key segments in radiology**:

| Segment | Purpose | Key fields |
|---|---|---|
| MSH | Message header | Message type (ORM, ORU, ADT), version |
| PID | Patient identification | Patient ID, name, DOB, sex |
| PV1 | Patient visit | Location, attending physician |
| ORC | Common order | Order control (NW/XO/CA), placer order # |
| OBR | Observation request | Procedure code, accession #, scheduling |
| OBX | Observation result | Report text, coded findings, status |

**Trigger events** (what causes a message to be sent):

| Trigger | Event | Message |
|---|---|---|
| A01 | Patient admit | ADT^A01 |
| A02 | Patient transfer | ADT^A02 |
| A03 | Patient discharge | ADT^A03 |
| A08 | Patient info update | ADT^A08 |
| A34 | Patient merge (ID only) | ADT^A34 |
| O01 | New order | ORM^O01 |
| O01 | Order modification | ORM^O01 (ORC-1=XO) |
| O01 | Order cancel | ORM^O01 (ORC-1=CA) |
| R01 | Unsolicited result | ORU^R01 |

**Acknowledgment modes**:

- **Original mode**: Receiver returns ACK with MSA segment indicating
  accept (AA), reject (AR), or error (AE)
- **Enhanced mode**: Application-level acknowledgment separate from
  transport acknowledgment

### DICOM (Digital Imaging and Communication in Medicine)

The standard for imaging data exchange and storage. Tag-based, service-
oriented, with Application Entities (AEs) communicating over TCP/IP.

**Key DICOM services in radiology**:

| Service | Role | Purpose |
|---|---|---|
| C-STORE | SCU → SCP | Send images to PACS |
| C-FIND | SCU ← SCP | Query worklist/patient/study |
| C-MOVE | SCU → SCP | Retrieve images from PACS |
| C-GET | SCU ← SCP | Retrieve images (alternate) |
| MPPS | SCU → SCP | Modality reports procedure status |
| Storage Commitment | SCU ← SCP | PACS confirms image receipt |

**Application Entity (AE) titles**: Each DICOM system has an AE title
(a unique identifier, up to 16 characters). When a modality can't reach
the PACS, the first thing to check is AE title, IP, and port configuration.

**DICOM Modality Worklist (MWL)**: The bridge between HL7 orders and
DICOM acquisition. The RIS (or MWL broker) exposes scheduled procedures
as DICOM worklist items. Modalities query via C-FIND and receive patient
demographics + procedure details. The modality then sends images with
matching identifiers.

**HL7-to-DICOM field mapping** (common conversions):

| HL7 field | DICOM tag | Content |
|---|---|---|
| PID-3 | (0010,0020) | Patient ID |
| PID-5 | (0010,0010) | Patient Name |
| PID-7 | (0010,0030) | Birth Date |
| PID-8 | (0010,0040) | Sex |
| OBR-4 | (0032,1060) | Requested Procedure Description |
| OBR-18 | (0008,0050) | Accession Number |
| OBR-27 | (0040,0002/0003) | Scheduled Procedure Step Start Date/Time |

### IHE (Integrating the Healthcare Enterprise)

Not a standard itself, but a framework that profiles how HL7 and DICOM
should be used together. IHE defines actors (system roles) and
transactions (messages) for specific workflows.

**Key IHE Radiology profiles**:

| Profile | Code | What it does |
|---|---|---|
| Scheduled Workflow | SWF/SWF.b | End-to-end order → acquisition → storage |
| Patient Information Reconciliation | PIR | Match unidentified patient images |
| Access to Radiology Information | ARI | Query reports and information |
| Key Image Note | KIN | Flag clinically significant images |
| Reporting Workflow | RWF | Report lifecycle management |
| Charge Posting | CHG | Send charges to billing |
| Evidence Documents | ED | Store non-image evidence |
| Mammography Image | MAMMO | Mammography-specific workflows |
| Cross-Enterprise Document Sharing for Imaging | XDS-I.b | Share images across organizations |

**IHE actors relevant to radiology**:

| Actor | Typical system | Role |
|---|---|---|
| Order Placer | EHR/CPOE | Creates imaging orders |
| Order Filler | RIS | Schedules and manages orders |
| Department System Scheduler | RIS | Manages worklist |
| Image Manager/Archive | PACS/VNA | Stores and retrieves images |
| Image Display | Workstation | Views images |
| Report Creator | Dictation/reporting | Generates reports |
| Performed Procedure Step Manager | RIS/modality | Tracks acquisition status |

### FHIR (Fast Healthcare Interoperability Resources)

The modern RESTful API standard, increasingly used alongside (not replacing)
HL7v2. JSON-based, resource-oriented.

**FHIR resources relevant to radiology**:

| Resource | Purpose |
|---|---|
| Patient | Patient demographics |
| ServiceRequest | Imaging order (replaces HL7 ORM) |
| DiagnosticReport | Radiology report |
| ImagingStudy | Reference to DICOM study |
| ImagingSelection | Subset of study for specific use |
| Encounter | Patient encounter context |

**FHIRcast**: A profile for real-time context synchronization between
applications (e.g., when radiologist opens study in PACS, reporting
platform auto-opens same study). Uses WebSocket-based hub-and-spoke
architecture.

## Depth 3 — where standards break down in practice

### HL7 version fragmentation

- Most radiology interfaces still run HL7v2.3.1 or v2.5.1 — not v3 or FHIR
- Each vendor interprets optional fields differently (e.g., OBR-18 for
  accession number is technically "Placer Field 1" by HL7 spec, but
  universally used for accession number by site convention)
- Z-segments (custom/vendor-specific) are common and undocumented in
  standard references

### DICOM conformance variations

- Each vendor publishes a DICOM Conformance Statement — these must be
  compared when troubleshooting cross-vendor connectivity
- AE title, port, and IP configuration is the #1 source of "modality can't
  connect" issues
- Storage Commitment is not universally implemented — some sites still
  rely on polling to confirm image receipt

### IHE profile adoption gaps

- IHE profiles define the "should" — real implementations vary
- SWF.b is the current profile, but many deployed systems still run SWF
  (HL7v2.3.1) or have partial profile coverage
- The IHE Integration Statement for each product version documents what's
  actually implemented — this is the authoritative source, not marketing

### Middleware/integration engine role

- Many sites use middleware (Rhapsody, Mirth Connect, InterSystems) to
  translate between systems — the "interface" in the site profile often
  refers to a middleware-managed connection, not a direct system link
- Middleware can mask problems (retry queues, message transformation) that
  would be immediately visible in a direct connection
- When a ticket says "interface is down," check whether the middleware is
  the actual point of failure

## Not this skill

This document covers standards generically — it does not document any
site's specific interface configuration. The site profile's `interfaces`
section is where that lives. When answering a user question about "how does
HL7 work at our site," check the profile first; use this document only for
generic standards context.

Message-level forensics (parsing raw HL7/DICOM messages) is the separate
forensics plugin's domain — this document explains what the standards say,
not how to debug individual messages.
