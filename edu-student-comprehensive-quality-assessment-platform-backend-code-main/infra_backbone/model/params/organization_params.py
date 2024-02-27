from typing import List

from infra_basic.basic_repository import PageFilterParams


class OrganizationQueryParams(PageFilterParams):
    category: List[str]
