"""
部门 实体类
"""
from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_backbone.entity.history.dept_history import DeptHistoryEntity


class DeptEntity(VersionedEntity):
    """
    部门
    """

    __tablename__ = "st_dept"
    __table_args__ = {"comment": "部门信息"}
    __history_entity__ = DeptHistoryEntity

    organization_id = Column(String(40), comment="组织id", nullable=False, index=True)
    name = Column(String(255), nullable=False, comment="部门名称")
    code = Column(String(255), nullable=True, comment="部门编码", index=True)
    comments = Column(String(255), nullable=True, comment="描述")
