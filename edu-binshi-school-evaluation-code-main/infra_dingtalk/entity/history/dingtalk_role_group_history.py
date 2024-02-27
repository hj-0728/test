"""
角色组历史表
"""


from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, String


class DingtalkRoleGroupHistoryEntity(HistoryEntity):
    """
    角色组历史表
    """

    __tablename__ = "st_dingtalk_role_group_history"
    __table_args__ = {"comment": "角色组历史表"}
    dingtalk_corp_id = Column(String(40), comment="钉钉组织id", nullable=False, index=True)
    remote_role_group_id = Column(String(255), comment="远程角色组id", nullable=False)
    name = Column(String(255), comment="角色组名称", nullable=False)
