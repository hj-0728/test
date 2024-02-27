from typing import List, Optional

from infra_basic.basic_repository import PageFilterParams


class RouteQueryParams(PageFilterParams):
    id: Optional[str]
    category: Optional[str]
    path: Optional[str]
    entry_code: Optional[str]
    access_strategy: Optional[str]
    role_name: Optional[List]
