from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String, Text


class CreationsHistoryEntity(HistoryEntity):
    """
    作品历史
    """

    __tablename__ = "st_creations_history"
    __table_args__ = {"comment": "作品历史"}
    creator_res_category = Column(
        String(255), comment="创建者资源类别（DIMENSION_DEPT_TREE/ESTABLISHMENT_ASSIGN）", nullable=False
    )
    creator_res_id = Column(String(40), comment="创建者资源id", nullable=False)
    created_on = Column(DateTime(timezone=True), comment="创建时间", nullable=False)
    comment = Column(Text, comment="备注", nullable=True)


Index(
    "idx_creations_history_time_range",
    CreationsHistoryEntity.id,
    CreationsHistoryEntity.commenced_on,
    CreationsHistoryEntity.ceased_on.desc(),
    unique=True,
)
