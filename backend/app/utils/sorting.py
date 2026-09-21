"""Shared query sorting helpers."""
from typing import Any

from sqlalchemy.orm import Query


def apply_sort(
    query: Query,
    columns: dict[str, Any],
    sort_by: str | None,
    sort_dir: str | None,
    default: str,
) -> Query:
    """Order a query using a whitelist of sortable columns."""
    column = columns.get(sort_by or default, columns[default])
    descending = str(sort_dir or "desc").lower() != "asc"
    return query.order_by(column.desc() if descending else column.asc())
