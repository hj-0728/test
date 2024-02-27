from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class CalcScoreLogHistoryEntity(HistoryEntity):
    __tablename__ = "st_calc_score_log_history"
    __table_args__ = {"comment": "计算节点得分记录（历史）"}

    evaluation_assignment_id = Column(String(40), nullable=False, comment="计划id", index=True)
    benchmark_calc_node_id = Column(String(40), nullable=False, comment="计算节点的id", index=True)


Index(
    "idx_calc_score_log_history_time_range",
    CalcScoreLogHistoryEntity.id,
    CalcScoreLogHistoryEntity.begin_at,
    CalcScoreLogHistoryEntity.end_at.desc(),
    unique=True,
)
