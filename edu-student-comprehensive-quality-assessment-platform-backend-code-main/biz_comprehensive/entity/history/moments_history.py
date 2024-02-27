from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String, Text


class MomentsHistoryEntity(HistoryEntity):
    """
    点滴历史
    """

    __tablename__ = "st_moments_history"
    __table_args__ = {"comment": "点滴历史"}
    owner_res_category = Column(
        String(255), comment="所有者资源类别（DIMENSION_DEPT_TREE/ESTABLISHMENT_ASSIGN）", nullable=False
    )
    owner_res_id = Column(String(40), comment="所有者资源id", nullable=False)
    recorded_on = Column(DateTime(timezone=True), comment="记录时间", nullable=False)
    comment = Column(Text, comment="备注", nullable=True)


Index(
    "idx_moments_history_time_range",
    MomentsHistoryEntity.id,
    MomentsHistoryEntity.commenced_on,
    MomentsHistoryEntity.ceased_on.desc(),
    unique=True,
)
