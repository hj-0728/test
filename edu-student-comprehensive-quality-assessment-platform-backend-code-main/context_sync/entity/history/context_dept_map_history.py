from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ContextDeptMapHistoryEntity(HistoryEntity):
    """
    上下文部门关联（历史实体类）
    """

    __tablename__ = "st_context_dept_map_history"
    __table_args__ = {"comment": "上下文部门关联（历史）"}
    dept_id = Column(String(255), comment="部门id", nullable=False)
    res_category = Column(String(255), comment="关联部门类型", nullable=False)
    res_id = Column(String(40), comment="关联部门id", nullable=True)


Index(
    "idx_context_dept_map_history_time_range",
    ContextDeptMapHistoryEntity.id,
    ContextDeptMapHistoryEntity.commenced_on,
    ContextDeptMapHistoryEntity.ceased_on.desc(),
    unique=True,
)
