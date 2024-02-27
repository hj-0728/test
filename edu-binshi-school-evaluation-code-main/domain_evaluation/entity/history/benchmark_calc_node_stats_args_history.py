from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.postgresql import JSONB


class BenchmarkCalcNodeStatsArgsHistoryEntity(HistoryEntity):
    __tablename__ = "st_benchmark_calc_node_stats_args_history"
    __table_args__ = {"comment": "计算方式为统计时的计算参数（历史）"}

    benchmark_calc_node_id = Column(String(40), nullable=False, comment="计算节点的id", index=True)
    stats_method = Column(String(255), nullable=False, comment="统计方法（avg、sum……）")
    stats_args = Column(JSONB, nullable=True, comment="统计参数")


Index(
    "idx_benchmark_calc_node_stats_args_history_time_range",
    BenchmarkCalcNodeStatsArgsHistoryEntity.id,
    BenchmarkCalcNodeStatsArgsHistoryEntity.begin_at,
    BenchmarkCalcNodeStatsArgsHistoryEntity.end_at.desc(),
    unique=True,
)
