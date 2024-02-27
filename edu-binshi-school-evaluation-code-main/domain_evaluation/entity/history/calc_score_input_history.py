from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class CalcScoreInputHistoryEntity(HistoryEntity):
    __tablename__ = "st_calc_score_input_history"
    __table_args__ = {"comment": "计算节点来源（历史）"}

    calc_score_log_id = Column(String(40), nullable=False, comment="计划id", index=True)
    source_score_category = Column(String(255), nullable=False,
                                   comment="计算节点的类型")
    source_score_id = Column(String(40), nullable=False, comment="来源分数id")


Index(
    "idx_calc_score_input_history_time_range",
    CalcScoreInputHistoryEntity.id,
    CalcScoreInputHistoryEntity.begin_at,
    CalcScoreInputHistoryEntity.end_at.desc(),
    unique=True,
)
