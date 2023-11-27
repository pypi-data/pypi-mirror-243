from typing import TypeVar, Optional, Union, List, Annotated

from fastapi import Query, Depends
from pydantic import constr
from starlette.requests import Request

from fastutils_hmarcuzzo.constants.regex_expressions import (
    REGEX_ORDER_BY_QUERY,
    REGEX_ALPHANUMERIC_WITH_UNDERSCORE as ALPHANUMERIC_WITH_UNDERSCORE,
)
from fastutils_hmarcuzzo.decorators.simple_pagination_decorator import SimplePaginationOptions
from fastutils_hmarcuzzo.types.custom_pages import custom_page_query, custom_size_query
from fastutils_hmarcuzzo.types.find_many_options import FindManyOptions
from fastutils_hmarcuzzo.utils.pagination_utils import PaginationUtils

E = TypeVar("E")
F = TypeVar("F")
O = TypeVar("O")
C = TypeVar("C")


class PaginationWithSearchOptions(SimplePaginationOptions):
    def __init__(
        self,
        entity: E,
        columns_query: C,
        find_all_query: F = None,
        order_by_query: O = None,
    ):
        self.entity = entity
        self.columns_query = columns_query
        self.find_all_query = find_all_query
        self.order_by_query = order_by_query

        self.pagination_utils = PaginationUtils()

    def __call__(
        self,
        page: int = custom_page_query,
        size: int = custom_size_query,
        search: Annotated[
            List[
                constr(pattern=f"^{ALPHANUMERIC_WITH_UNDERSCORE}:{ALPHANUMERIC_WITH_UNDERSCORE}$")
            ],
            Query(example=["field:value"]),
        ] = None,
        sort: Annotated[
            List[constr(pattern=f"^{ALPHANUMERIC_WITH_UNDERSCORE}:{REGEX_ORDER_BY_QUERY}")],
            Query(example=["field:by"]),
        ] = None,
        columns: Annotated[
            List[constr(pattern=f"^{ALPHANUMERIC_WITH_UNDERSCORE}$")],
            Query(example=["field"]),
        ] = None,
        search_all: Annotated[
            constr(pattern=f"^{ALPHANUMERIC_WITH_UNDERSCORE}$"),
            Query(example=["value"]),
        ] = None,
    ) -> FindManyOptions:
        paging_params = self.pagination_utils.generate_paging_parameters(
            page,
            size,
            search,
            sort,
            self.find_all_query,
            self.order_by_query,
        )

        return self.pagination_utils.get_paging_data(
            self.entity,
            paging_params,
            columns if columns else [],
            search_all,
            self.columns_query,
            self.find_all_query,
        )
