# Proposal

## Why

Kellular has a vision (README, info/) but no code, data contract or way to measure progress. Before
building models, it needs a shared representation of a patient's tumor, a record of which data
it may use and under what terms, and a benchmark that scores predictions against real mCRC patient
outcomes. Without the benchmark, later phases have no way to tell a working twin from a plausible one.

## What Changes

- Scaffold the local repository: Python package (`src/kellular`), uv environment, tests, Apache-2.0
  license with NOTICE, data directories kept out of version control, placeholders for pipelines and
  Terraform.
- Fix the v0 scope to **metastatic colorectal cancer with liver and/or lung metastases**.
- Define the **TumorProfile** data model: patient → samples (primary, liver met, lung met, plasma
  ctDNA) → timepoints → molecular layers, with the mCRC biomarkers used in care today.
- Create a **data-source catalog** that records ownership, license, citation and access tier. A
  source cannot be ingested until it is registered.
- Define the **benchmark**: outcome-linked mCRC patients, patient-level splits, a guideline biomarker
  baseline, and the metrics every future predictor must report.
- Run a **data-access audit** to confirm which outcome-linked mCRC cohorts are actually usable.

Non-goals:
- No models, embeddings or response predictions. Those come in Phase 3.
- No raw FASTQ processing. Phase 0 uses public processed data only.
- No cloud deployment, and no Git remote.
- No spatial/VCM simulation or molecule design.

Data dependencies: TCGA COAD/READ (open tier), cBioPortal mCRC studies (MSK-CHORD, MSK-MET; access
to be confirmed), AACR GENIE BPC CRC (controlled). See docs/DATA_SOURCES.md.

## Capabilities

### New Capabilities
- `tumor-profile`: canonical, serializable representation of one patient's tumor across sites and
  time, including mCRC biomarkers and references to molecular data files.
- `data-catalog`: registry of external data sources with ownership, license, citation and access
  tier, enforced at ingestion and carried as provenance on every profile.
- `benchmark`: evaluation of treatment-response predictions against real mCRC patient outcomes, with
  leakage-safe splits and a mandatory biomarker-rule baseline.

### Modified Capabilities
<!-- none: first change in the project -->

## Impact

- New Python package and dev environment (pydantic runtime dependency; anndata/scanpy optional).
- New docs: docs/ROADMAP.md, docs/DATA_SOURCES.md.
- Establishes contracts that Phase 1 ingestion, Phase 2 profiling and Phase 3 prediction will depend
  on.
