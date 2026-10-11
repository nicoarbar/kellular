"""Ingestion gate: every loader calls this before touching the network."""

from __future__ import annotations

from collections.abc import Mapping

from kellular.catalog import Catalog, Source, UnknownSourceError


class IngestRefused(Exception):
    """Ingestion of a source was refused before anything was downloaded."""


class UnregisteredSourceError(IngestRefused):
    pass


class UnverifiedLicenseError(IngestRefused):
    pass


class MissingCredentialsError(IngestRefused):
    pass


def require_ingestible(
    catalog: Catalog,
    source_id: str,
    credentials: Mapping[str, str] | None = None,
) -> Source:
    """Return the source if it may be ingested, otherwise raise IngestRefused.

    Refuses sources that are unregistered, whose license is unverified, or that are
    controlled-access and have no credentials configured.
    """
    try:
        source = catalog.get(source_id)
    except UnknownSourceError as exc:
        raise UnregisteredSourceError(
            f"{exc}. Register it in catalog/sources.yaml and docs/DATA_SOURCES.md first."
        ) from exc

    if source.license_status != "verified":
        raise UnverifiedLicenseError(
            f"license of {source.name!r} is unverified. Confirm it from the owner's terms "
            f"({source.url}) and set license_status: verified in catalog/sources.yaml."
        )

    if source.access == "controlled" and not credentials:
        raise MissingCredentialsError(
            f"{source.name!r} is controlled-access and no credentials are configured. "
            f"Request access from {source.owner} at {source.url}; do not use mirrors."
        )

    return source
