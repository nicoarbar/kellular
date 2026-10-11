# Kellular roadmap

**Scope (v0):** metastatic colorectal cancer (mCRC) with liver and/or lung metastases.
**Research use only.** Kellular produces hypotheses for researchers and clinicians, not treatment
decisions.

## Guiding principle

Build the smallest thing whose output can be checked against real patient outcomes, then widen.
The differentiator is closing the **cell line/organoid → patient** gap, not another predictor
trained and scored on cell lines.

## Phases

| Phase | Name | Output | Stage (info/vcm-infra.md) |
|---|---|---|---|
| 0 | Foundation | Repo, `TumorProfile` schema, data-source catalog, benchmark definition | - |
| 1 | Data layer | Loaders for public mCRC cohorts, cell lines, organoids and knowledge bases | D |
| 2 | Profiling | Twin v0: subclones, CMS subtype, microenvironment, per metastatic site | A |
| 3 | Response prediction | Drug ranking scored on the patient benchmark | B |
| 4 | Trial matching | TumorProfile → eligible ClinicalTrials.gov trials | B |
| 5 | Spatial/VCM layer | Perturbation + neighbourhood models, synthetic data behind real-data gates | A/B |
| 6 | De novo design | Neoantigen/mRNA vaccine and binder design | C |
| 7 | Validation loop | Wet-lab/organoid feedback, longitudinal ctDNA updates of the twin | D |

Change proposals for each phase live in `openspec/changes/`. Accepted behavior lives in
`openspec/specs/`.

## Why mCRC with liver/lung metastases

- Clear molecular decision points already used in care (MSI/dMMR, RAS, BRAF V600E, HER2,
  KRAS G12C, sidedness), which give a strong baseline to beat.
- Liver and lung are the dominant metastatic sites, and paired primary/metastasis data exist.
- Patient-derived organoids are well established in CRC, which is the most direct route to studying
  the in vitro → patient gap.
- ctDNA is routinely used in CRC, which makes longitudinal twin updates realistic later.

## Compute

Local only for Phases 0-2. Terraform templates in `infra/terraform/` (AWS, Hugging Face, neo-clouds)
from Phase 3 onward, when foundation-model embeddings and training need GPUs.
