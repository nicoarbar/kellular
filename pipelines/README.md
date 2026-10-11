# Pipelines

Configs for upstream processing of raw sequencing data with nf-core:

- `nf-core/sarek` - WES/WGS variant calling (tumor/normal, somatic SNVs, CNVs, MSI)
- `nf-core/rnaseq` - bulk RNA-seq quantification
- `nf-core/scrnaseq` - single-cell RNA-seq alignment and count matrices

Outputs land in `data/interim/` and are loaded into the TumorProfile schema by `kellular.ingest`.
Not used in Phase 0 (public processed data only).
