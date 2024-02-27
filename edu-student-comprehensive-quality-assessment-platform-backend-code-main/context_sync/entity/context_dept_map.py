"""
上下文部门关联
"""
from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from context_sync.entity.history.context_dept_map_history import ContextDeptMapHistoryEntity


class ContextDeptMapEntity(VersionedEntity):
    """
    上下文部门关联
    """

    __tablename__ = "st_context_dept_map"
    __table_args__ = {"comment": "上下文部门关联"}
    __history_entity__ = ContextDeptMapHistoryEntity
    dept_id = Column(String(40), comment="部门id", nullable=False)
    res_category = Column(String(255), comment="关联部门类型", nullable=False)
    res_id = Column(String(40), comment="关联部门id", nullable=True)
