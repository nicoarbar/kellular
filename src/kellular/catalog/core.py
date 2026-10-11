"""Registry of external data sources: ownership, license, citation, access tier."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

DEFAULT_CATALOG_PATH = Path(__file__).resolve().parents[3] / "catalog" / "sources.yaml"


class CatalogError(Exception):
    """Base class for catalog errors."""


class UnknownSourceError(CatalogError):
    """The requested source id is not registered."""


class Source(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    name: str = Field(min_length=1)
    owner: str = Field(min_length=1)
    url: str = Field(min_length=1)
    license: str = Field(min_length=1)
    citation: str = Field(min_length=1)
    access: Literal["open", "controlled"]
    redistribution: Literal["allowed", "forbidden", "unknown"]
    license_status: Literal["verified", "unverified"]
    notes: str = ""


class Catalog:
    def __init__(self, sources: Iterable[Source]):
        self._sources: dict[str, Source] = {}
        for source in sources:
            if source.id in self._sources:
                raise CatalogError(f"duplicate source id: {source.id}")
            self._sources[source.id] = source

    def __iter__(self) -> Iterator[Source]:
        return iter(self._sources.values())

    def __len__(self) -> int:
        return len(self._sources)

    def __contains__(self, source_id: object) -> bool:
        return source_id in self._sources

    def get(self, source_id: str) -> Source:
        try:
            return self._sources[source_id]
        except KeyError:
            raise UnknownSourceError(
                f"source {source_id!r} is not registered in the catalog"
            ) from None


def load_catalog(path: Path | str = DEFAULT_CATALOG_PATH) -> Catalog:
    """Load and validate the catalog. Raises pydantic.ValidationError on an invalid entry."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return Catalog(Source.model_validate(entry) for entry in data.get("sources", []))


def attributions(catalog: Catalog, source_ids: Iterable[str]) -> str:
    """Markdown attribution block (owner, license, citation) for the given sources."""
    lines = []
    for source_id in source_ids:
        s = catalog.get(source_id)
        suffix = "" if s.license_status == "verified" else " (license not yet verified)"
        lines.append(
            f"- **{s.name}**, {s.owner}. License: {s.license}{suffix}. {s.citation} <{s.url}>"
        )
    return "\n".join(lines)
