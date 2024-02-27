from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB

from domain_evaluation.entity.history.benchmark_calc_node_stats_args_history import (
    BenchmarkCalcNodeStatsArgsHistoryEntity,
)


class BenchmarkCalcNodeStatsArgsEntity(VersionedEntity):
    __tablename__ = "st_benchmark_calc_node_stats_args"
    __table_args__ = {"comment": "计算方式为统计时的计算参数"}
    __history_entity__ = BenchmarkCalcNodeStatsArgsHistoryEntity

    benchmark_calc_node_id = Column(String(40), nullable=False, comment="计算节点的id", index=True)
    stats_method = Column(String(255), nullable=False, comment="统计方法（avg、sum……）")
    stats_args = Column(JSONB, nullable=True, comment="统计参数")
