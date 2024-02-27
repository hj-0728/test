"""
钉钉用户与钉钉角色的绑定关系
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_dingtalk.entity.history.dingtalk_user_role_history import DingtalkUserRoleHistoryEntity


class DingtalkUserRoleEntity(VersionedEntity):
    """
    钉钉用户与钉钉角色的绑定关系
    """

    __tablename__ = "st_dingtalk_user_role"
    __table_args__ = {"comment": "钉钉用户与钉钉角色的绑定关系"}
    __history_entity__ = DingtalkUserRoleHistoryEntity
    dingtalk_user_id = Column(String(40), comment="钉钉user_id", nullable=False)
    dingtalk_role_id = Column(String(40), comment="钉钉角色id", nullable=False)
