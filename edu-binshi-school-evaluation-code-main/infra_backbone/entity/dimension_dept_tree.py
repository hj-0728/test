from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Integer, String, text

from infra_backbone.entity.history.dimension_dept_tree_history import DimensionDeptTreeHistoryEntity


class DimensionDeptTreeEntity(VersionedEntity):
    __tablename__ = "st_dimension_dept_tree"
    __table_args__ = {"comment": "维度树"}
    __history_entity__ = DimensionDeptTreeHistoryEntity

    dimension_id = Column(String(40), nullable=False, comment="维度id", index=True)
    dept_id = Column(String(40), nullable=False, comment="部门id", index=True)
    parent_dept_id = Column(String(40), nullable=True, comment="上级部门id", index=True)
    seq = Column(Integer, nullable=False, comment="排序码", server_default=text("1"), index=True)
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始于")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束于",
        server_default=text("'infinity'::timestamptz"),
    )
