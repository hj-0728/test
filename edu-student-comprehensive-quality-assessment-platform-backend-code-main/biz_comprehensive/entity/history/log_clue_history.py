from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class LogClueHistoryEntity(HistoryEntity):
    """
    日志线索历史
    """

    __tablename__ = "st_log_clue_history"
    __table_args__ = {"comment": "日志线索历史"}
    log_res_category = Column(
        String(255),
        comment="日志资源类别（POINTS_LOG/INDICATOR_SCORE_LOG/MEDAL_ISSUE_LOG）",
        nullable=False,
    )
    log_res_id = Column(String(40), comment="日志资源id", nullable=False)
    clue_res_category = Column(String(255), comment="线索类别（CALC_LOG）", nullable=False)
    clue_res_id = Column(String(40), comment="线索id", nullable=False)


Index(
    "idx_log_clue_history_time_range",
    LogClueHistoryEntity.id,
    LogClueHistoryEntity.commenced_on,
    LogClueHistoryEntity.ceased_on.desc(),
    unique=True,
)
