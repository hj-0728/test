from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String, Text

from biz_comprehensive.entity.history.moments_history import MomentsHistoryEntity


class MomentsEntity(VersionedEntity):
    """
    点滴
    """

    __tablename__ = "st_moments"
    __table_args__ = {"comment": "点滴"}
    __history_entity__ = MomentsHistoryEntity
    owner_res_category = Column(
        String(255), comment="所有者资源类别（DIMENSION_DEPT_TREE/ESTABLISHMENT_ASSIGN）", nullable=False
    )
    owner_res_id = Column(String(40), comment="所有者资源id", nullable=False)
    recorded_on = Column(DateTime(timezone=True), comment="记录时间", nullable=False)
    comment = Column(Text, comment="备注", nullable=True)
