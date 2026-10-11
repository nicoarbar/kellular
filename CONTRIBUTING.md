# Contributing to Kellular

Thanks for your interest. Kellular is early-stage research software, so small, focused
contributions are the easiest to review.

## Ground rules

1. **Never commit patient data or third-party data.** No genomic, transcriptomic, proteomic or
   clinical files, no credentials, no API keys. `data/` is gitignored on purpose. If you are unsure
   whether something is safe to publish, do not push it and ask first.
2. **Register data sources before using them.** To add an external source, add an entry to
   `catalog/sources.yaml` and a matching row to `docs/DATA_SOURCES.md` (the test
   `tests/test_catalog_docs.py` fails if they disagree). Confirm its license from the owner's terms.
   Kellular never redistributes third-party data.
3. **Research use only.** Do not present outputs as medical advice. See
   [DISCLAIMER.md](DISCLAIMER.md).

## Workflow

1. Open an issue to discuss larger changes. Behavior changes are proposed in `openspec/changes/`
   (see [docs/ROADMAP.md](docs/ROADMAP.md)).
2. Fork the repo and create a branch from `main`.
3. Make your change with tests.
4. Run the checks locally:

   ```bash
   uv sync
   uv run pytest
   uv run ruff check .
   uv run ruff format --check .
   ```

5. Open a pull request against `main`, describe what and why, and resolve review conversations.
   `main` is protected: changes land through pull requests, and force pushes are disabled.

## Style

- Python 3.11+, formatted and linted with `ruff` (line length 100).
- Type-annotate public functions. Keep modules small and documented.
- Write clear commit messages: a short imperative summary line, then the why if it is not obvious.

## Licensing of contributions

Kellular is licensed under the [Apache License 2.0](LICENSE). Unless you state otherwise, any
contribution you submit is licensed under the same terms (Apache 2.0, section 5). Only contribute
code you have the right to license this way. If you add code from a third party, say so in the PR
and in [NOTICE](NOTICE) when the license requires attribution.

## Reporting security issues

Do not open a public issue for vulnerabilities or exposed data. Follow [SECURITY.md](SECURITY.md).
