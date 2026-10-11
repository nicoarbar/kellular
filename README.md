# CLAUDE.md

### Kellular
Kellular has the objective to build a simulation model that can create and validate molecules that outsmart cancer with personal oncology data. It is about building this model that can become a digital twin from the tumor that can replicate or simulate digitally its dynamic behaviour. 

The purpose for this model would be to simulate:

1. Which drugs can be an effective treatment given its genomic, transcriptomic and proteomic expresion. 
2. Are there any active clinical trials or promising molecules tested in wet labs that can work to reduce or deprecate the tumor. 
3. Build from scratch the molecule, treatment, ARN vaccine that can work in this case. 

It´s about allowing any oncology patient to build its tumor twin model to monitor its behaviour digitally. Having this twin will allow to understand and simulate what can work. 
The problem is how to build the tumor twin and how to update it with real-time data so it stays up to date with the biological twin. 

Its about building the infrastructure to make this possible for oncology patients. They would need to have a sample or biopsy of their own tumor, and get their genetic, transcriptomic, or proteomic data with sequencing or single-cell tools. Once we have that data, we can build their "tumor-twin".

Here are the generic steps to build Kellular:
1. Collect the omics data
2. Process the omics data
3. Build the model with the omics data
4. Infer data from the model built
5. Simulate synthetic data from perturbation data
6. Discover which biological target may work to reduce tumor growth
7. Design the drug based on the biological target
8. Infer prognosis and efficacy of the drug
9. Produce the drug with wet lab and validate its efficacy in a clinical trial

The ultimate goal is to build a model that can outsmart cancer in a personalized manner since every tumor and patient are different. 

## 1. Data provider
- You need omic data from oncology patients to train the model. Real data, not just synthetic data. 
- We will need the genetic sequence, or single-cell transcriptomic or proteomic data from the biopsies, or liquid biopsies from ctDNA. 
- Maybe we need to build an automated workflow to get the biological physical data. 
- Pharma and biotech companies and hospitals and research centers already have data from the clinical trials and wet lab experiments. 
- Data sources: 
    - genomics (Ensembl, genetic databases)
    - transcriptomic (single cell tools)
    - proteomic (Uniprot, Alpha Fold)
    - chemical (ChemBL)
    - molecular pathways (Reactome)
    - clinical trials (clinicaltrials.gov)
    - research literature (PubMed, BioRxiv)


## 2. Virtual Cell Models (VCMs)
- Deployment of VCMs as a cluster with the omics data. If we could have one virtual cell model, then scale it as a cluster of VCMs, then we could have a tumor twin. 
- Simulate perturbation data
- Generate Synthetic data from the perturbation
    - The problem of unvalidated synthetic data. This will be a self-consuming loop that will generate "model collapse". Which is the model trainer recursively with pertubation data from its predecesor. There will be a convergence into a homogenous distribution. 
    - Low biological diversity
    - Its like a model distillation.

## 3. Tumor twin
- Build the tumor twin from the VCM Cluster
- Simulate which molecules can work

## 4. Personalized molecule, drug, treatment, vaccine
- Once the tumor twin makes simulations and predictions, infer the personalized cure. 
- Build a model that can create the molecule that outsmarts cancer.
- AlphaFold for protein prediction

## 5. Agent for Wet Lab Validation
- Validation on the wet lab from the simuation of the tumor twin
- Validation that the tumor twin has the same dynamic and behaviour with the real tumor
- Validation that the personalized molecule, drug, treatment, vaccine can work in the oncology patient. 

### Limitations
- How to get the physical tissue or biopsy.
- From the biopsy get and run the omics data.
- The biopsy does not show the whole diverse picture of a tumor profile, it is just a sample.
- Combine with ctDNA or liquid biopsy to enrich the data from to make up the tumor profile in the tumor twin. 
- The data might be noisy and messy. To train and build better models and run better simulations, we need better quality data. We need to improve the processing of data. 

## MCP tooling available in this workspace

The Claude Code session also has ad hoc biomedical research MCP servers connected (bioRxiv, ChEMBL,
Clinical Trials, Open Targets, PubMed, Synapse.org) — useful for grounding the ideas in `info/vcm-premises.md` and `info/vcm-infra.md` in actual literature, compound/target data, and trial data
rather than speculation.

- `vcm-premises.md` (Spanish) — notes exploring Virtual Cell Models: simulating tissues/tumors/
  organoids as digital twins, matching patients to clinical trials via a simulated tissue profile,
  and the core open problem — where enough real perturbation/experimental data would come from to
  train such models, and whether synthetic data generated by the models themselves is good enough
  to train further models.
