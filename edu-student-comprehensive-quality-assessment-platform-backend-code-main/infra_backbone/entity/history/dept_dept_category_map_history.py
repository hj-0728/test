"""
部门和部门类型信息关系   历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class DeptDeptCategoryMapHistoryEntity(HistoryEntity):
    """
    部门和部门类型信息关系 历史
    """

    __tablename__ = "st_dept_dept_category_map_history"
    __table_args__ = {"comment": "部门和部门类型信息关系 历史"}

    dept_id = Column(String(40), comment="部门id", nullable=False, index=True)
    dept_category_id = Column(String(40), nullable=False, comment="部门类型id")


Index(
    "idx_dept_dept_category_map_history_time_range",
    DeptDeptCategoryMapHistoryEntity.id,
    DeptDeptCategoryMapHistoryEntity.commenced_on,
    DeptDeptCategoryMapHistoryEntity.ceased_on.desc(),
    unique=True,
)
