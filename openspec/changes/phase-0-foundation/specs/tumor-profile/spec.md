# Spec Delta

## Purpose

Provide one canonical, serializable representation of a patient's tumor across anatomical sites and
time. Every Kellular stage reads it, and it is the structural backbone of the tumor twin.

## ADDED Requirements

### Requirement: Patient-sample-timepoint hierarchy
A TumorProfile SHALL describe exactly one patient and contain one or more samples. Each sample SHALL
record its sample type (tumor tissue, normal tissue, or plasma cfDNA), its anatomical site, and the
timepoint at which it was collected, expressed as days relative to the patient's diagnosis.

#### Scenario: Paired primary and liver metastasis
- **WHEN** a profile is built from a colon primary resected at day 0 and a liver metastasis biopsied at day 210
- **THEN** the profile contains two tumor-tissue samples with sites `colon` and `liver` and timepoints 0 and 210

#### Scenario: Sample without a timepoint
- **WHEN** a sample is provided without a collection timepoint
- **THEN** validation fails with an error naming the sample

### Requirement: Supported anatomical sites for v0
The profile SHALL accept primary sites colon (with left/right sidedness) and rectum, metastatic sites
liver and lung, and plasma for liquid biopsy. It SHALL reject a primary site outside colorectal
cancer. Other metastatic sites SHALL be accepted but flagged as outside v0 scope.

#### Scenario: Out-of-scope primary
- **WHEN** a profile declares a primary tumor in the breast
- **THEN** validation fails with an out-of-scope error

#### Scenario: Peritoneal metastasis
- **WHEN** a sample from a peritoneal metastasis is included
- **THEN** the profile is valid and carries an out-of-scope warning for that sample

### Requirement: mCRC clinical biomarkers
Each tumor sample SHALL be able to carry MSI/MMR status, KRAS/NRAS/BRAF status (including the
specific variant, e.g. BRAF V600E, KRAS G12C), HER2 (ERBB2) amplification status, and consensus
molecular subtype (CMS1-4). Each biomarker value SHALL record whether it was measured or inferred,
and its source. An unknown biomarker SHALL be represented explicitly as unknown, never as absent or
negative.

#### Scenario: Unmeasured MSI status
- **WHEN** no MSI or MMR assay result is available for a sample
- **THEN** its MSI status reads `unknown`, and downstream consumers can tell it apart from `MSS`

#### Scenario: Inferred subtype
- **WHEN** CMS is computed from expression data rather than reported by the source
- **THEN** the CMS value is marked `inferred` and names the method used

### Requirement: Molecular layers by reference
A sample SHALL reference its molecular data layers (somatic variants, copy number, bulk expression,
single-cell expression, proteomics) by file location and format rather than embedding the matrices.
Each reference SHALL state the genome build and gene identifier namespace.

#### Scenario: Single-cell layer
- **WHEN** a liver-metastasis sample has scRNA-seq data
- **THEN** the sample references an h5ad file with genome build GRCh38 and Ensembl gene IDs

### Requirement: Treatment and outcome history
A profile SHALL record treatment lines (regimen, agents, start/end day, line number) and outcome
events (response category, progression, death, last follow-up) on the same day-relative timeline as
the samples. This is what lets the twin line up samples with the treatments given before and after
them.

#### Scenario: First-line treatment before metastasis biopsy
- **WHEN** a patient receives first-line FOLFOX plus bevacizumab from day 30 to day 180 and a liver biopsy is taken on day 210
- **THEN** the profile can answer that the liver sample was collected after first-line treatment

### Requirement: Round-trip serialization
A TumorProfile SHALL serialize to JSON and deserialize to an equivalent profile, and the JSON SHALL
carry a schema version.

#### Scenario: Round trip
- **WHEN** a valid profile is serialized and read back
- **THEN** the result equals the original and reports the same schema version

### Requirement: Provenance on every profile
Every sample and molecular layer SHALL name the data-catalog source it came from.

#### Scenario: Unregistered source
- **WHEN** a profile references a source that is not registered in the data catalog
- **THEN** validation fails with an error naming the unknown source
