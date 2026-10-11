import pytest
import yaml
from pydantic import ValidationError

from kellular.catalog import (
    Catalog,
    CatalogError,
    UnknownSourceError,
    attributions,
    load_catalog,
)


def entry(**overrides):
    base = {
        "id": "demo",
        "name": "Demo source",
        "owner": "Demo Institute",
        "url": "https://example.org/",
        "license": "CC BY 4.0",
        "citation": "Demo et al. (2020).",
        "access": "open",
        "redistribution": "unknown",
        "license_status": "verified",
    }
    return {**base, **overrides}


def write_catalog(tmp_path, *entries):
    path = tmp_path / "sources.yaml"
    path.write_text(yaml.safe_dump({"sources": list(entries)}), encoding="utf-8")
    return path


def test_shipped_catalog_loads_and_is_fully_unverified():
    catalog = load_catalog()
    assert len(catalog) == 16
    assert all(s.license_status == "unverified" for s in catalog)


def test_entry_missing_license_is_rejected(tmp_path):
    bad = entry()
    del bad["license"]
    with pytest.raises(ValidationError, match="license"):
        load_catalog(write_catalog(tmp_path, bad))


def test_entry_with_empty_citation_is_rejected(tmp_path):
    with pytest.raises(ValidationError, match="citation"):
        load_catalog(write_catalog(tmp_path, entry(citation="")))


def test_invalid_access_tier_is_rejected(tmp_path):
    with pytest.raises(ValidationError, match="access"):
        load_catalog(write_catalog(tmp_path, entry(access="semi-open")))


def test_duplicate_ids_are_rejected(tmp_path):
    with pytest.raises(CatalogError, match="duplicate"):
        load_catalog(write_catalog(tmp_path, entry(), entry(name="Other")))


def test_unknown_source_lookup(tmp_path):
    catalog = load_catalog(write_catalog(tmp_path, entry()))
    with pytest.raises(UnknownSourceError, match="nope"):
        catalog.get("nope")


def test_attribution_for_tcga_and_depmap():
    text = attributions(load_catalog(), ["tcga-coad-read", "depmap"])
    assert "Nature 487, 330-337 (2012)" in text
    assert "Cell 170, 564-576 (2017)" in text
    assert "Broad Institute" in text


def test_attribution_flags_unverified_license(tmp_path):
    catalog = load_catalog(write_catalog(tmp_path, entry(license_status="unverified")))
    assert "license not yet verified" in attributions(catalog, ["demo"])


def test_attribution_unknown_source_raises():
    with pytest.raises(UnknownSourceError):
        attributions(Catalog([]), ["depmap"])
