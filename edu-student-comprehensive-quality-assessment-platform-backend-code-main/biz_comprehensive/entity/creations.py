from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String, Text

from biz_comprehensive.entity.history.creations_history import CreationsHistoryEntity


class CreationsEntity(VersionedEntity):
    """
    作品
    """

    __tablename__ = "st_creations"
    __table_args__ = {"comment": "作品"}
    __history_entity__ = CreationsHistoryEntity
    creator_res_category = Column(
        String(255), comment="创建者资源类别（DIMENSION_DEPT_TREE/ESTABLISHMENT_ASSIGN）", nullable=False
    )
    creator_res_id = Column(String(40), comment="创建者资源id", nullable=False)
    created_on = Column(DateTime(timezone=True), comment="创建时间", nullable=False)
    comment = Column(Text, comment="备注", nullable=True)
