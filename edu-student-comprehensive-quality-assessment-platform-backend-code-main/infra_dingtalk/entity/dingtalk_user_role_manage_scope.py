"""
钉钉用户角色的管理范围
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_dingtalk.entity.history.dingtalk_user_role_manage_scope_history import (
    DingtalkUserRoleManageScopeHistoryEntity,
)


class DingtalkUserRoleManageScopeEntity(VersionedEntity):
    """
    钉钉用户角色管理范围关系
    """

    __tablename__ = "st_dingtalk_user_role_manage_scope"
    __table_args__ = {"comment": "钉钉用户角色的管理范围"}
    __history_entity__ = DingtalkUserRoleManageScopeHistoryEntity
    dingtalk_user_role_id = Column(String(40), comment="钉钉用户角色id", nullable=False)
    dingtalk_dept_id = Column(String(40), comment="钉钉部门id", nullable=False)
