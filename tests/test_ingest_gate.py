import pytest

from kellular.catalog import Catalog, Source
from kellular.ingest.gate import (
    IngestRefused,
    MissingCredentialsError,
    UnregisteredSourceError,
    UnverifiedLicenseError,
    require_ingestible,
)


def source(**overrides):
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
    return Source(**{**base, **overrides})


def test_verified_open_source_passes():
    catalog = Catalog([source()])
    assert require_ingestible(catalog, "demo").id == "demo"


def test_unregistered_source_is_refused():
    with pytest.raises(UnregisteredSourceError, match="not registered"):
        require_ingestible(Catalog([]), "demo")


def test_unverified_license_is_refused():
    catalog = Catalog([source(license_status="unverified")])
    with pytest.raises(UnverifiedLicenseError, match="unverified"):
        require_ingestible(catalog, "demo")


def test_controlled_source_without_credentials_is_refused_with_instructions():
    catalog = Catalog([source(access="controlled")])
    with pytest.raises(MissingCredentialsError, match="Request access from Demo Institute"):
        require_ingestible(catalog, "demo")


def test_controlled_source_with_credentials_passes():
    catalog = Catalog([source(access="controlled")])
    assert require_ingestible(catalog, "demo", credentials={"token": "x"}).id == "demo"


def test_all_refusals_share_a_base_class():
    for exc in (UnregisteredSourceError, UnverifiedLicenseError, MissingCredentialsError):
        assert issubclass(exc, IngestRefused)


def test_every_shipped_source_is_currently_refused():
    from kellular.catalog import load_catalog

    catalog = load_catalog()
    for s in catalog:
        with pytest.raises(UnverifiedLicenseError):
            require_ingestible(catalog, s.id, credentials={"token": "x"})
