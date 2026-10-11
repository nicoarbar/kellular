# Data sources

Every external source must be listed here **before** it is ingested. Kellular never redistributes
third-party data. Loaders download from the owner's official endpoint, and derived artifacts keep a
pointer back to this table.

**Register before ingest.** The machine-readable source of truth is `catalog/sources.yaml`; this
file is its readable view, and a test (`tests/test_catalog_docs.py`) fails if the two disagree. To
add a source: add an entry to `catalog/sources.yaml` and a row here, with the same name. Ingestion
(`kellular.ingest.gate.require_ingestible`) refuses any source that is unregistered, whose
`license_status` is `unverified`, or that is controlled-access without credentials. The licenses and
citations in the catalog are provisional until task 3.1 confirms them from the owners' terms.

Column notes:
- **Access**: `open` (download without an application) or `controlled` (DUA, registration, dbGaP).
- **License**: `verify` means it has not yet been confirmed from the owner's official terms. It must
  be confirmed before the source is ingested.

## Patient cohorts (outcome-linked; the benchmark depends on these)

| Source | Content relevant to mCRC | Access | License | Status |
|---|---|---|---|---|
| TCGA COAD/READ (GDC) | Primary tumor WES, RNA-seq, CNV, methylation, limited clinical | open + controlled | NIH GDC terms, verify | candidate |
| CPTAC colon (PDC) | Proteomics + phosphoproteomics paired with genomics | open | verify | candidate |
| MSK-CHORD (cBioPortal) | Clinicogenomic data with treatments, outcomes, metastatic sites | open | CC BY-NC-ND 4.0 (stated by owner), verify | candidate, key for benchmark; non-commercial |
| MSK-MET (cBioPortal) | Metastatic-site-annotated tumor sequencing | open | CC BY-NC-ND 4.0 (stated by owner), verify | candidate; no treatment data, non-commercial |
| AACR Project GENIE (incl. BPC CRC) | Panel sequencing, curated treatment/outcome for the BPC cohort | controlled | GENIE terms | candidate |

## Preclinical perturbation data

| Source | Content | Access | License | Status |
|---|---|---|---|---|
| DepMap (CRISPR, PRISM) | CRC cell line dependencies and drug response | open | CC BY 4.0, verify | candidate |
| GDSC | Drug sensitivity for CRC cell lines | open | verify | candidate |
| Tahoe-100M | Single-cell drug perturbation atlas | open | verify | candidate |
| CRC organoid drug-response studies (e.g. Vlachogiannis 2018, Ooft 2019) | PDO response matched to patient response | verify | verify | candidate, key for the in vitro → patient gap |

## Single-cell / spatial references

| Source | Content | Access | License | Status |
|---|---|---|---|---|
| CELLxGENE Census | scRNA-seq incl. CRC primary and liver metastasis datasets | open | per dataset, verify | candidate |
| Published CRC liver-metastasis scRNA/spatial studies (GEO) | Paired primary/liver-met microenvironment | open | per study, verify | to identify |

## Knowledge bases

| Source | Content | Access | License | Status |
|---|---|---|---|---|
| Ensembl | Gene IDs, GRCh38 annotation | open | verify | candidate |
| Open Targets | Target-disease evidence | open | verify | candidate |
| ChEMBL | Compounds, mechanisms, bioactivity | open | CC BY-SA 3.0, verify | candidate |
| Reactome | Pathways | open | verify | candidate |
| ClinicalTrials.gov | Trial eligibility and status | open | public domain (US gov), verify | candidate |
