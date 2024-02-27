from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.class_team_category_history import (
    ClassTeamCategoryHistoryEntity,
)


class ClassTeamCategoryEntity(VersionedEntity):
    """
    班级小组类型
    """

    __tablename__ = "st_class_team_category"
    __table_args__ = {"comment": "班级小组类型"}
    __history_entity__ = ClassTeamCategoryHistoryEntity
    name = Column(String(255), comment="小组类型名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    dimension_dept_tree_id = Column(String(40), comment="部门范围id", nullable=False)
    creator_people_id = Column(String(40), comment="创建人id", nullable=False)
