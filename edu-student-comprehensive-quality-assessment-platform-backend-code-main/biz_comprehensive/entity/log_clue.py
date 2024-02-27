from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.log_clue_history import LogClueHistoryEntity


class LogClueEntity(VersionedEntity):
    """
    日志线索
    """

    __tablename__ = "st_log_clue"
    __table_args__ = {"comment": "日志线索"}
    __history_entity__ = LogClueHistoryEntity
    log_res_category = Column(
        String(255),
        comment="日志资源类别（POINTS_LOG/INDICATOR_SCORE_LOG/MEDAL_ISSUE_LOG）",
        nullable=False,
    )
    log_res_id = Column(String(40), comment="日志资源id", nullable=False)
    clue_res_category = Column(String(255), comment="线索类别（CALC_LOG）", nullable=False)
    clue_res_id = Column(String(40), comment="线索id", nullable=False)
