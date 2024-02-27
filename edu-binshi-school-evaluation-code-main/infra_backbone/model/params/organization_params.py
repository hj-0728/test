from typing import List, Optional

from infra_basic.basic_repository import PageFilterParams


class OrganizationQueryParams(PageFilterParams):
    category: List[str]


class CurrentUserRoleOperateSchoolQueryParams(PageFilterParams):
    id: Optional[str]
    name: Optional[str]
    is_operated: Optional[bool]
    user_id: Optional[str]
