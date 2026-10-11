# Spec Delta

## Purpose

Record who owns each external dataset or model Kellular uses, under what license and access terms,
and how to cite it. This keeps ownership explicit and makes ingestion refuse unregistered sources.

## ADDED Requirements

### Requirement: Source registration
The catalog SHALL hold one entry per external source with: identifier, owner, official URL, license,
required citation, access tier (`open` or `controlled`), whether redistribution is permitted, and a
license verification status (`verified` or `unverified`).

#### Scenario: Listing sources
- **WHEN** a user lists the catalog
- **THEN** every entry shows its owner, license, access tier and verification status

### Requirement: Ingestion gate
Ingestion SHALL refuse a source that is missing from the catalog or whose license is `unverified`.

#### Scenario: Unverified license
- **WHEN** ingestion is requested for a source whose license status is `unverified`
- **THEN** ingestion stops before downloading anything and reports that the license must be verified

### Requirement: No redistribution of third-party data
Kellular SHALL NOT include third-party data files in its distributable artifacts. Loaders SHALL
obtain data from the owner's official endpoint, under the user's own credentials for controlled
sources.

#### Scenario: Controlled-access source without credentials
- **WHEN** a controlled-access source is ingested without credentials configured
- **THEN** ingestion fails with instructions for requesting access from the owner, and no data is fetched from any mirror

### Requirement: Attribution export
The catalog SHALL be able to produce the citations and attributions for any set of sources used in
an analysis.

#### Scenario: Citations for a benchmark run
- **WHEN** a benchmark run used TCGA and DepMap
- **THEN** the run's report includes the required citations for both sources
