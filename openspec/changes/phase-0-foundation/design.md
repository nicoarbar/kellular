# Design

## Context

Greenfield repository: only notes (README, info/) exist. See proposal.md - Why. Constraints: local
compute only, no Git remote yet, and code must be open while respecting third-party data
ownership.

## Goals / Non-Goals

**Goals:**
- A schema that is small enough to fill from public processed data now and rich enough to hold
  single-cell, proteomic and longitudinal ctDNA data later without breaking changes.
- A benchmark definition that can be computed once a usable outcome-linked cohort is confirmed.

**Non-Goals:**
- Storage backends beyond the local filesystem (no database, no object store yet).
- A CLI or API surface. Library functions and tests are enough for Phase 0.

## Decisions

**D1. Python + uv, src layout.** The single-cell/omics ecosystem (scanpy, anndata, scvi-tools) is
Python-first. uv gives reproducible locks and fast environments. The src layout prevents tests from
importing the working tree by accident. *Alternatives:* conda (heavier, slower solves, still usable
later for nf-core tooling); poetry (slower, no advantage here).

**D2. Pydantic v2 for TumorProfile, with matrices kept by reference.** Profiles are small JSON
documents that point at h5ad/Parquet/MAF files. This keeps profiles cheap to diff, validate and send
to an LLM agent, while large matrices stay in formats the omics tools already read. *Alternatives:*
one big AnnData/MuData per patient (hard to hold multi-site, multi-timepoint structure and treatment
history); a relational DB (premature before the access patterns are known).

**D3. Day-relative timeline anchored at diagnosis.** Samples, treatments and outcomes all use integer
days from diagnosis. This avoids storing real dates (a re-identification risk), matches how cBioPortal
and GENIE BPC publish timelines, and makes "sample before or after treatment" a simple comparison.

**D4. Explicit `unknown` plus measured/inferred provenance on biomarkers.** Public cohorts are
patchy, and silently treating a missing value as negative would corrupt both the baseline and the
learned models.

**D5. Data catalog as a versioned YAML file (`catalog/sources.yaml`), with docs/DATA_SOURCES.md as
its human-readable view.** The ingestion gate and attribution export read the YAML. A test checks that
the Markdown table and the YAML agree until the Markdown is generated automatically.
*Alternative:* Markdown only (not machine-enforceable).

**D6. Licensing: Apache-2.0 for code, NOTICE for attribution, no data redistribution.** Apache-2.0
requires attribution to be preserved and includes a patent grant, which matters in a drug-discovery
setting. Third-party datasets and model weights keep their own licenses, recorded per source. Models
with non-commercial weights (e.g. STATE/ST-Tahoe) must be flagged in the catalog before use.
*Alternatives:* MIT (no patent grant, weaker NOTICE convention); AGPL (would block pharma/hospital
collaboration).

**D7. Benchmark baseline = guideline biomarker rules.** mCRC already uses molecularly guided
treatment, so the honest baseline is "what a guideline-following oncologist would pick", not a random
or majority-class baseline.

## Risks / Trade-offs

- [Outcome-linked mCRC data with pre-treatment molecular data may be scarce or controlled-access] →
  The data-access audit runs first. If only controlled cohorts qualify, apply for GENIE BPC early and
  build the harness on TCGA/MSK open data in the meantime, clearly labelled as provisional.
- [Most public cohorts sequence the primary tumor, not the liver/lung metastasis] → The schema
  records the site of every sample, so the benchmark can measure how much a primary-only profile
  limits prediction.
- [Panel sequencing (MSK-IMPACT, GENIE) lacks expression data, so CMS can't be computed] → The
  benchmark notes, per patient, which molecular layers are available. Expression-dependent models are
  evaluated only on the subset that has expression data.
- [Schema churn once real data arrives] → The schema is versioned from day one (tumor-profile spec,
  round-trip requirement).

## Open Questions

- The exact license terms of each candidate source (tracked as `unverified` in the catalog until
  confirmed).
- Whether docs are also released under CC BY 4.0 in addition to code under Apache-2.0.
