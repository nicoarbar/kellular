# Kellular

Tumor digital twin for **metastatic colorectal cancer (mCRC)** with liver and/or lung metastases:
profile a tumor from omics data, predict which drugs may work, match clinical trials, and
(later) design candidate molecules and mRNA vaccines, with every step checked against real
patient outcomes.

> **Research use only.** Kellular produces hypotheses for researchers and clinicians. It is not a
> medical device and does not provide diagnosis, prognosis or treatment recommendations. See
> [DISCLAIMER.md](DISCLAIMER.md).

## Status

Early stage (**Phase 0, foundation**): package skeleton, `TumorProfile` schema, data-source
catalog and ingestion gate. Nothing here is validated for clinical use.

- Vision and long-term goals: [docs/VISION.md](docs/VISION.md)
- Phases and scope: [docs/ROADMAP.md](docs/ROADMAP.md)
- External data sources and their licenses: [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md)
- Change proposals and specs: [openspec/](openspec/)

## Getting started

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest
uv run ruff check .
```

Optional single-cell / omics dependencies: `uv sync --extra omics`.

## Data and privacy

Kellular **never redistributes third-party datasets** and the repository **never contains patient
data**. Raw, interim and processed data live only on your machine (`data/` is gitignored). Every
external source must be registered in `catalog/sources.yaml` and `docs/DATA_SOURCES.md` before it
is ingested, and the ingestion gate refuses unregistered or unverified sources.

## Contributing and security

- How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md)
- Reporting a vulnerability or exposed data: [SECURITY.md](SECURITY.md)

## License

Apache License 2.0, see [LICENSE](LICENSE) and [NOTICE](NOTICE).
