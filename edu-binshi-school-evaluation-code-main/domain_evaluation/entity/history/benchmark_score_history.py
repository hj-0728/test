from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Numeric, String


class BenchmarkScoreHistoryEntity(HistoryEntity):
    __tablename__ = "st_benchmark_score_history"
    __table_args__ = {"comment": "基准分数（历史）"}

    evaluation_assignment_id = Column(String(40), nullable=False, comment="计划id", index=True)
    benchmark_id = Column(String(40), nullable=False, comment="基准id", index=True)
    numeric_score = Column(Numeric, nullable=True, comment="数字型的分数")
    string_score = Column(String(255), nullable=True, comment="字符串类型的分数")
    source_score_log_category = Column(String(255), nullable=False, comment="input/calc")
    source_score_log_id = Column(String(40), nullable=False, comment="来源分数日志id")


Index(
    "idx_benchmark_score_history_time_range",
    BenchmarkScoreHistoryEntity.id,
    BenchmarkScoreHistoryEntity.begin_at,
    BenchmarkScoreHistoryEntity.end_at.desc(),
    unique=True,
)
