# RIS Software Catalog

Generic domain reference. Site-specific system names come from the site
profile, not from here — if you're answering a user, cite which parts of
this you're grounding generically vs. from their profile.

## Depth 1 — one line

Radiology IT environments typically combine a RIS (order/scheduling
workflow), a PACS (image archive/viewing), an EHR (order origin/results
destination), and a reporting platform — each from potentially different
vendors, connected via HL7 and DICOM interfaces.

## Depth 2 — major RIS platforms

### Fujifilm Synapse

- **Product**: Synapse EIS/RIS + Synapse PACS
- **Vendor**: Fujifilm Healthcare Americas
- **Role**: Integrated RIS/PACS with enterprise imaging capabilities
- **Key interfaces**: HL7v2 inbound (ADT, ORM) and outbound (ORM status
  updates), DICOM MWL/MPPS, FHIR (newer versions)
- **Integration notes**: Synapse PACS uses HIIS (HIS/RIS Interface Service)
  for HL7 communication. Supports both message-based (TCP/IP) and file-based
  integration modes. Status change messages (Complete, Dictated, Started,
  Sent) are sent outbound on a separate port from inbound messages.
- **Documentation**: `https://healthcaresolutions-us.fujifilm.com/wp-content/uploads/2023/02/Synapse_RIS_Version_4-0.pdf`

### Epic Radiant

- **Product**: Radiant (RIS module within Epic EHR)
- **Vendor**: Epic Systems
- **Role**: EHR-integrated RIS — orders, scheduling, worklist, result
  routing. Does not store/display images (requires separate PACS).
- **Key interfaces**: HL7v2 ORM/ORU for orders/results, DICOM MWL/MPPS,
  WADO for image linking, FHIR APIs via open.epic
- **Integration notes**: Radiant generates DICOM MWL for scanners. Reports
  route back via HL7 ORU or DICOM SR. Image links in Epic chart launch
  PACS viewer via Enterprise Image Access API with SSO context sync.
  28+ certified PACS vendors via open.epic program.
- **Documentation**: `https://open.epic.com/Ancillary/CardRad`

### Sectra RIS

- **Product**: Sectra RIS (Europe/Pacific markets)
- **Vendor**: Sectra AB
- **Role**: Standalone RIS with DICOM CDS (RIS DICOM Service) for
  MWL/MPPS connectivity
- **Key interfaces**: HL7v2, DICOM MWL SCP, DICOM MPPS SCP/SCU, IHE
  Scheduled Workflow
- **Integration notes**: CDS service runs on Windows, handles MWL queries
  and MPPS relay. Supports patient verification against RIS database
  before accepting MPPS. Default local AE title: SECTRA_RIS, port 4007.
- **Documentation**: `https://medical.sectra.com/iheintegrationstatement-ris-27-1/`

### AGFA HealthCare Enterprise Imaging

- **Product**: Enterprise Imaging (Core Server + Web Server + XERO Viewer)
- **Vendor**: AGFA HealthCare
- **Role**: Unified imaging platform — RIS/PACS/VNA in single architecture
- **Key interfaces**: HL7v2 (ADT, ORM, ORU, SIU with conversion), DICOM
  MWL/MPPS, FHIR R4/R5 (Scheduling module), IHE profiles
- **Integration notes**: Core Server may convert unsupported SIU triggers to
  ORM (with data loss). Limited patient linking support (A24 converts to
  A40). HL7 Conformance Profiles available as bundled zip for validation.
- **Documentation**: `https://www.agfahealthcare.com/hl7/` (HL7),
  `https://www.agfahealthcare.com/fhir-conformance-statement/` (FHIR)

### GE Healthcare Centricity

- **Product**: Centricity RIS-i / RIS-IC + Centricity PACS
- **Vendor**: GE HealthCare
- **Role**: Integrated RIS/PACS with modular architecture
- **Key interfaces**: HL7v2 via HL7 Interface Server, DICOM MWL/MPPS,
  ModLink for advanced data integration
- **Integration notes**: HL7 Interface Server converts HL7 messages to SQL
  stored procedures for PACS database. Supports DICOM MWL for modality
  worklist queries. RA1000 workstation handles Query/Retrieve.
- **Documentation**: `https://www.gehealthcare.com/en-us/products/interoperability/ihe-integration-statements/radiology-pacs-workstations-mammo-ris`

### Philips IntelliSpace

- **Product**: IntelliSpace Radiology + IntelliSpace PACS
- **Vendor**: Philips Healthcare
- **Role**: Integrated radiology workflow — RIS/PACS with clinical
  applications
- **Key interfaces**: HL7v2 (ADT, ORM, ORU), DICOM MWL/MPPS/SR, WADO,
  IHE profiles, API integrations via plug-ins
- **Integration notes**: Client/Server architecture with remote server
  management by Philips. Supports plug-in integrations via API (must be
  Windows 10 + IE 10/11 64-bit). Volume Vision 2D/3D/4D viewing included.
- **Documentation**: `https://www.usa.philips.com/healthcare/support/dicom/pacs-systems-and-web-viewing-ihe-integration-statements`

### Siemens Healthineers syngo

- **Product**: syngo.plaza / syngo.share (PACS) + syngo Workflow (RIS)
- **Vendor**: Siemens Healthineers
- **Role**: PACS-centric platform with RIS integration
- **Key interfaces**: HL7v2 (RIS settings configurable), DICOM MWL/MPPS,
  PIX Query, IHE profiles
- **Integration notes**: RIS communicates with PACS via HL7. Parallel RIS
  operation supported (RIS talks to both old and new PACS during
  migration). Patient updates should always be performed on RIS side.
- **Documentation**: `https://www.siemens-healthineers.com/services/it-standards/hl7-digital-and-automation/pacs`

### Change Healthcare Radiology Solutions (Optum)

- **Product**: Radiology Solutions PACS + Image Repository (VNA)
- **Vendor**: Optum (formerly Change Healthcare)
- **Role**: Enterprise PACS with vendor-neutral archive
- **Key interfaces**: HL7v2, DICOM, cloud-native Stratus Imaging Archive
- **Integration notes**: Stratus built on Google Cloud, integrates with any
  PACS and multiple EHRs via HL7. Supports collaborative radiology with
  real-time screen sharing.
- **Documentation**: `https://business.optum.com/en/operations-technology/enterprise-imaging/change-healthcare-radiology.html`

### Nuance PowerScribe (Microsoft)

- **Product**: PowerScribe 360 Reporting + PowerScribe One + PowerCast
- **Vendor**: Nuance/Microsoft
- **Role**: Reporting platform — dictation, report generation, distribution
- **Key interfaces**: XML/JSON file-based integration, FHIRcast (PowerCast),
  HL7 ORU for report delivery
- **Integration notes**: Supports both PowerScribe Driven (PS360 controls
  PACS launch) and Partner Driven (PACS controls PS360) modes. FHIRcast
  hub (PowerCast) enables real-time context sync between PACS, RIS, and
  reporting. Accession number + MRN used for multi-site deduplication.
- **Documentation**: `https://isupportcontent.nuance.com/Healthcare/Admin_Portal_Help/PACS_Integrations.htm`

### Rad AI Reporting

- **Product**: Rad AI Reporting + Rad AI Impressions + Rad AI Continuity
- **Vendor**: Rad AI
- **Role**: AI-augmented reporting — automated impressions, follow-up
  management
- **Key interfaces**: FHIRcast, FHIR Store, XML/JSON file integration,
  deep-link integration
- **Integration notes**: Desktop app only (not web) for file-based
  integrations. FHIRcast syncs context with PACS — when radiologist opens
  study in PACS, Rad AI auto-opens same study for reporting. SOC 2 Type II
  HIPAA+ certified.
- **Documentation**: `https://app.radai.com/docs/`

## Depth 3 — integration patterns and where they break

### Common integration topology

```
EHR/CPOE --[HL7 ORM]--> RIS --[DICOM MWL]--> Modality --[DICOM Storage]--> PACS
EHR     <--[HL7 ORU]--- RIS <--[MPPS status]---------------------------
```

### Where vendor differences matter

- **Accession number ownership**: Some RIS platforms generate accession
  numbers internally; others accept them from the EHR. When an accession
  number doesn't match between systems, check which system "owns" it in
  the site profile's `identifier_formats`.
- **Report routing path**: Some configurations route reports directly from
  the reporting platform to EHR (bypassing RIS). If "report not in EHR"
  doesn't fit the RIS-to-EHR interface, check for a separate
  reporting-platform-to-EHR interface.
- **MPPS behavior**: Not all modalities or PACS send MPPS consistently. A
  "study performed but not showing as complete" symptom may trace to missing
  MPPS rather than a RIS configuration issue.
- **HL7 message variants**: While HL7v2 is the standard, each vendor has
  site-configurable variations. The HL7 Interface Server or middleware
  (Rhapsody, Mirth Connect) often handles translation — check the site
  profile's `interfaces` section for middleware systems.

### IHE Radiology profiles (reference)

The IHE Radiology Technical Framework defines standard integration patterns.
Key profiles relevant to overnight support:

| Profile | Purpose |
|---|---|
| Scheduled Workflow (SWF/SWF.b) | End-to-end order workflow |
| Patient Information Reconciliation (PIR) | Match images to unidentified patients |
| Access to Radiology Information (ARI) | Query/report access |
| Key Image Note (KIN) | Flag important images |
| Reporting Workflow (RWF) | Report lifecycle management |
| Charge Posting (CHG) | Billing integration |

Reference: `https://profiles.ihe.net/RAD/index.html`

### HL7 message types in radiology

| Message | Direction | Purpose |
|---|---|---|
| ADT (A01-A47) | EHR/HIS → RIS/PACS | Patient admit/transfer/discharge/merge |
| ORM^O01 | EHR → RIS | New/modified/cancelled imaging order |
| ORU^R01 | RIS → EHR | Radiology report delivery |
| SIU (S12-S26) | RIS → Modality | Scheduling notifications |
| ACK | Both directions | Message acknowledgment |

## Not this skill

This document is a vendor catalog for domain context — it does not replace
the site profile's `systems` and `interfaces` sections, which describe
what *this* site actually runs. When answering a user question, always
ground in the site profile first; fall back to this catalog only when the
profile doesn't name the specific system being asked about, and say so.

This document does not cover message-level parsing or forensics — that is
the separate forensics plugin's domain.
