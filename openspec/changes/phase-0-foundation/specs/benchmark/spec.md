# Spec Delta

## Purpose

Score treatment-response predictions for mCRC against what actually happened to real patients, so
progress is measured on patients and not only on cell lines or synthetic data.

## ADDED Requirements

### Requirement: Outcome-linked evaluation cohort
The benchmark SHALL be built only from real patients with mCRC (liver and/or lung metastases) who
have molecular data collected before the evaluated treatment line, the treatment received, and an
observed outcome for that line. Synthetic or model-generated patients SHALL NOT be included.

#### Scenario: Molecular data collected after treatment
- **WHEN** a patient's only molecular sample was collected after the treatment line being evaluated
- **THEN** that patient-line pair is excluded from the benchmark

### Requirement: Leakage-safe splits
Train/validation/test splits SHALL be made at the patient level, so that all samples of one patient
fall in the same split. The test split SHALL be fixed and versioned once published.

#### Scenario: Patient with primary and metastasis samples
- **WHEN** a patient contributes both a primary and a liver-metastasis sample
- **THEN** both samples are assigned to the same split

### Requirement: Mandatory biomarker baseline
Every benchmark report SHALL include a baseline that assigns treatments using established mCRC
molecular decision rules (MSI-H/dMMR, RAS status with tumor sidedness, BRAF V600E, HER2
amplification, KRAS G12C). A predictor SHALL only be reported as an improvement if it beats this
baseline on the test split.

#### Scenario: Model underperforms the baseline
- **WHEN** a learned model scores below the biomarker baseline on the test split
- **THEN** the report shows the model as not improving on the baseline

### Requirement: Reported metrics
Each run SHALL report discrimination for response (AUROC with confidence intervals) and, where
time-to-event outcomes exist, concordance for progression-free survival, stratified by metastatic
site (liver, lung, both).

#### Scenario: Site-stratified report
- **WHEN** a benchmark run completes
- **THEN** the report contains overall metrics and separate metrics for liver-only, lung-only and liver-plus-lung patients

### Requirement: Transfer-gap reporting
When a predictor is trained on preclinical data (cell lines or organoids), its report SHALL show its
preclinical validation score next to its patient test score, so the preclinical → patient gap is
visible.

#### Scenario: Cell-line-trained model
- **WHEN** a model trained on DepMap/GDSC is benchmarked
- **THEN** the report lists both its cell-line hold-out score and its patient test score
