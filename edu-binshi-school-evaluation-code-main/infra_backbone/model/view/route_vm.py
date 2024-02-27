from typing import List, Optional

from infra_basic.basic_model import VersionedModel


class RouteViewModel(VersionedModel):
    category: str
    category_name: Optional[str]
    role_name_list: Optional[List]
    path: str
    entry_code: Optional[str]
    access_strategy: str
    access_strategy_name: Optional[str]
    ability_permission_list: Optional[List]
