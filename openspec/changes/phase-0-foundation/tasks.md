# Tasks

## 1. Repository scaffolding

- [x] 1.1 Create src layout (`src/kellular/{schema,ingest,profile,predict,trials}`), tests/, benchmarks/, pipelines/, infra/terraform/, docs/, data/{raw,interim,processed} and verify the tree exists
- [x] 1.2 Add Apache-2.0 LICENSE (canonical text from apache.org) and NOTICE with the third-party data policy, and verify both are referenced in pyproject.toml `license-files`
- [x] 1.3 Add .gitignore excluding data, omics file formats, Terraform state and secrets
- [x] 1.4 Add pyproject.toml (hatchling, pydantic runtime, `omics` extra, pytest/ruff dev group) and verify `uv sync` succeeds and `uv run pytest` passes the import smoke test
- [x] 1.5 Write docs/ROADMAP.md (mCRC liver/lung scope, phases 0-7) and docs/DATA_SOURCES.md (candidate sources, licenses marked verify)

## 2. Data catalog

- [x] 2.1 Create `catalog/sources.yaml` with every entry from docs/DATA_SOURCES.md (all `unverified`) and a loader that validates required fields; verify with a test that rejects an entry missing `license`
- [x] 2.2 Implement the ingestion gate (unknown or unverified source → refusal before any download); verify with tests for both refusal paths
- [x] 2.3 Implement attribution export for a set of source IDs; verify a test produces the TCGA + DepMap citations
- [x] 2.4 Add a consistency test between catalog/sources.yaml and docs/DATA_SOURCES.md and document the "register before ingest" rule in docs/DATA_SOURCES.md

## 3. Data-access audit

- [ ] 3.1 For each patient cohort in the catalog, confirm from the owner's official terms: license, access tier, whether treatment lines + outcomes + pre-treatment molecular data exist, and metastatic-site annotation; record findings in the catalog and flip verified licenses to `verified`
- [ ] 3.2 Count eligible mCRC (liver/lung) patient-line pairs per open cohort and write the result to docs/benchmark-cohort.md; verify the counts are reproducible from a script in benchmarks/
- [ ] 3.3 Decide the primary and fallback benchmark cohorts from 3.2 and record the decision in docs/benchmark-cohort.md; start controlled-access applications (e.g. GENIE BPC) if needed

## 4. TumorProfile schema

- [ ] 4.1 Implement patient/sample/timepoint models with v0 site rules (colon with sidedness, rectum, liver, lung, plasma; out-of-scope primary rejected, other met sites warned); verify with tests for each tumor-profile scenario
- [ ] 4.2 Implement biomarker fields (MSI/MMR, KRAS/NRAS/BRAF with variant, HER2, CMS) with explicit `unknown` and measured/inferred provenance; verify with tests
- [ ] 4.3 Implement molecular-layer references (path, format, genome build, gene ID namespace) and treatment/outcome timeline; verify the "sample collected after first-line" scenario in a test
- [ ] 4.4 Implement JSON round-trip with schema version and catalog-backed provenance validation; verify round-trip and unregistered-source tests
- [ ] 4.5 Add a hand-written example mCRC profile (primary + liver met + plasma, FOLFOX+bev first line) under tests/fixtures and document the schema in docs/tumor-profile.md

## 5. Benchmark harness

- [ ] 5.1 Implement eligibility filtering (pre-treatment molecular data, treatment line, observed outcome, liver/lung mCRC); verify the post-treatment-sample exclusion scenario in a test
- [ ] 5.2 Implement patient-level, seeded, versioned splits; verify that no patient appears in two splits
- [ ] 5.3 Implement the guideline biomarker baseline (MSI-H/dMMR, RAS + sidedness, BRAF V600E, HER2, KRAS G12C); verify each rule on synthetic unit-test profiles (test fixtures only, never benchmark data)
- [ ] 5.4 Implement the report: AUROC with bootstrap CIs, PFS C-index when available, stratified by liver/lung/both, transfer-gap columns, and source citations; verify on a small fixture cohort
- [ ] 5.5 Document how to run the benchmark in benchmarks/README.md and verify the documented command runs

## 6. Integration check

- [ ] 6.1 Load the chosen open cohort end-to-end (catalog gate → TumorProfiles → benchmark baseline report) and verify a report is produced with citations; run `openspec validate phase-0-foundation --strict`
