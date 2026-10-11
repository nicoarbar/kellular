"""docs/DATA_SOURCES.md must list exactly the sources in catalog/sources.yaml."""

from pathlib import Path

from kellular.catalog import load_catalog

DOCS = Path(__file__).resolve().parents[1] / "docs" / "DATA_SOURCES.md"


def doc_source_names():
    names = []
    for line in DOCS.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        first = line.strip("|").split("|")[0].strip()
        if first not in ("Source", ""):
            names.append(first)
    return names


def test_docs_table_matches_catalog():
    assert sorted(doc_source_names()) == sorted(s.name for s in load_catalog())


def test_docs_state_the_register_before_ingest_rule():
    text = DOCS.read_text(encoding="utf-8")
    assert "catalog/sources.yaml" in text
    assert "Register before ingest" in text
