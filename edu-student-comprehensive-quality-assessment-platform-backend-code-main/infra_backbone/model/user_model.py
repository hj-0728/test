from datetime import datetime
from typing import List, Optional

from infra_basic.basic_model import VersionedModel


class UserModel(VersionedModel):
    """
    用户信息
    """

    name: Optional[str]
    is_activated: bool = True
    valid_until: Optional[datetime]
    password: Optional[str]
    salt: Optional[str]
    try_count: Optional[int]
    password_reset: bool = True

    people_id: Optional[str]
    people_name: Optional[str]

    role_id_list: Optional[List[str]]
    role_name_list: Optional[List[str]]
