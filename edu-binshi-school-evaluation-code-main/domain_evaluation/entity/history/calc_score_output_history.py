from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Numeric, String


class CalcScoreOutputHistoryEntity(HistoryEntity):
    __tablename__ = "st_calc_score_output_history"
    __table_args__ = {"comment": "计算节点输出（历史）"}

    calc_score_log_id = Column(String(40), nullable=False, comment="计划id", index=True)
    numeric_score = Column(Numeric, nullable=True, comment="数字型的分数")
    string_score = Column(String(255), nullable=True, comment="字符串类型的分数")


Index(
    "idx_calc_score_output_history_time_range",
    CalcScoreOutputHistoryEntity.id,
    CalcScoreOutputHistoryEntity.begin_at,
    CalcScoreOutputHistoryEntity.end_at.desc(),
    unique=True,
)
