"""Data-source catalog: who owns each dataset, under what license, and how to cite it.

Spec: openspec/changes/phase-0-foundation/specs/data-catalog/spec.md
"""

from kellular.catalog.core import (
    DEFAULT_CATALOG_PATH,
    Catalog,
    CatalogError,
    Source,
    UnknownSourceError,
    attributions,
    load_catalog,
)

__all__ = [
    "DEFAULT_CATALOG_PATH",
    "Catalog",
    "CatalogError",
    "Source",
    "UnknownSourceError",
    "attributions",
    "load_catalog",
]
