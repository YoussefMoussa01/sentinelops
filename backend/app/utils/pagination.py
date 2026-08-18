"""Pagination utilities."""
from math import ceil
from typing import Generic, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Query
from app.schemas.common import PaginationParams, PaginationMeta

T = TypeVar("T", bound=BaseModel)


class PaginatedResult(BaseModel, Generic[T]):
    """Paginated result wrapper."""

    items: list[T]
    pagination: PaginationMeta


def paginate(
    query: Query, params: PaginationParams
) -> tuple[list, PaginationMeta]:
    """Paginate a SQLAlchemy query."""
    total = query.count()
    total_pages = ceil(total / params.page_size)

    items = query.offset(
        (params.page - 1) * params.page_size
    ).limit(params.page_size).all()

    pagination = PaginationMeta(
        page=params.page,
        page_size=params.page_size,
        total=total,
        total_pages=total_pages,
    )

    return items, pagination
