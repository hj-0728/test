"""
角色组
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_dingtalk.entity.history.dingtalk_role_group_history import DingtalkRoleGroupHistoryEntity


class DingtalkRoleGroupEntity(VersionedEntity):
    """
    角色组
    """

    __tablename__ = "st_dingtalk_role_group"
    __table_args__ = {"comment": "角色组"}
    __history_entity__ = DingtalkRoleGroupHistoryEntity
    dingtalk_corp_id = Column(String(40), comment="钉钉组织id", nullable=False, index=True)
    remote_role_group_id = Column(String(255), comment="远程角色组id", nullable=False)
    name = Column(String(255), comment="角色组名称", nullable=False)
