"""
钉钉用户角色的管理范围
"""

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class DingtalkUserRoleManageScopeHistoryEntity(HistoryEntity):
    """
    钉钉用户角色的管理范围
    """

    __tablename__ = "st_dingtalk_user_role_manage_scope_history"
    __table_args__ = {"comment": "钉钉用户角色的管理范围历史表"}
    dingtalk_user_role_id = Column(String(40), comment="钉钉用户角色id", nullable=False)
    dingtalk_dept_id = Column(String(40), comment="钉钉部门id", nullable=False)


# 时间检索索引
Index(
    "idx_dingtalk_user_role_manage_scope_history_time_range",
    DingtalkUserRoleManageScopeHistoryEntity.id,
    DingtalkUserRoleManageScopeHistoryEntity.commenced_on,
    DingtalkUserRoleManageScopeHistoryEntity.ceased_on.desc(),
    unique=True,
)
