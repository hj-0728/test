"""
用户查询
"""
from typing import List, Optional

from infra_basic.basic_repository import PageFilterParams


class UserQueryParams(PageFilterParams):
    is_activated: Optional[bool]
    current_user_role_code: Optional[str]
    filter_out_role_code: Optional[List[str]]
