"""
钉钉用户与钉钉角色的绑定关系
"""

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, String


class DingtalkUserRoleHistoryEntity(HistoryEntity):
    """
    钉钉用户与钉钉角色的绑定关系
    """

    __tablename__ = "st_dingtalk_user_role_history"
    __table_args__ = {"comment": "钉钉用户与钉钉角色的绑定关系历史表"}
    dingtalk_user_id = Column(String(40), comment="钉钉user_id", nullable=False)
    dingtalk_role_id = Column(String(40), comment="钉钉角色id", nullable=False)
