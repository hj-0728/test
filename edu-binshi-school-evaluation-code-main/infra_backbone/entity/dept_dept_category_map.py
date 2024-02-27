"""
部门和部门类型信息关系 实体类
"""
from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, String, text

from infra_backbone.entity.history.dept_category_history import DeptCategoryHistoryEntity
from infra_backbone.entity.history.dept_dept_category_map_history import (
    DeptDeptCategoryMapHistoryEntity,
)


class DeptDeptCategoryMapEntity(VersionedEntity):
    """
    部门和部门类型信息关系
    """

    __tablename__ = "st_dept_dept_category_map"
    __table_args__ = {"comment": "部门和部门类型信息关系"}
    __history_entity__ = DeptDeptCategoryMapHistoryEntity

    dept_id = Column(String(40), comment="部门id", nullable=False, index=True)
    dept_category_id = Column(String(40), nullable=False, comment="部门类型id")
