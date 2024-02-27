"""
部门类型   历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Index, String, text


class DeptCategoryHistoryEntity(HistoryEntity):
    """
    部门类型 历史
    """

    __tablename__ = "st_dept_category_history"
    __table_args__ = {"comment": "部门类型 历史"}

    organization_id = Column(String(40), comment="组织id", nullable=False, index=True)
    name = Column(String(255), nullable=False, comment="部门类型名称")
    code = Column(String(255), nullable=True, comment="部门类型编码", index=True)
    is_available = Column(Boolean, nullable=False, comment="是否可用", server_default=text("true"))


Index(
    "idx_dept_category_history_time_range",
    DeptCategoryHistoryEntity.id,
    DeptCategoryHistoryEntity.begin_at,
    DeptCategoryHistoryEntity.end_at.desc(),
    unique=True,
)
