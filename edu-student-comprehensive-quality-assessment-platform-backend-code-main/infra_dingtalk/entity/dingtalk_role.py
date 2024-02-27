"""
角色
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_dingtalk.entity.history.dingtalk_role_history import DingtalkRoleHistoryEntity


class DingtalkRoleGroupEntity(VersionedEntity):
    """
    角色
    """

    __tablename__ = "st_dingtalk_role"
    __table_args__ = {"comment": "角色"}
    __history_entity__ = DingtalkRoleHistoryEntity
    dingtalk_role_group_id = Column(String(40), comment="角色组id", nullable=False, index=True)
    remote_role_id = Column(String(255), comment="远程角色id", nullable=False)
    name = Column(String(255), comment="角色名称", nullable=False)
