"""
部门类型 实体类
"""
from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, String, text

from infra_backbone.entity.history.dept_category_history import DeptCategoryHistoryEntity


class DeptCategoryEntity(VersionedEntity):
    """
    部门类型
    """

    __tablename__ = "st_dept_category"
    __table_args__ = {"comment": "部门类型信息"}
    __history_entity__ = DeptCategoryHistoryEntity

    organization_id = Column(String(40), comment="组织id", nullable=False, index=True)
    name = Column(String(255), nullable=False, comment="部门类型名称")
    code = Column(String(255), nullable=True, comment="部门类型编码", index=True)
    is_available = Column(Boolean, nullable=False, comment="是否可用", server_default=text("true"))
