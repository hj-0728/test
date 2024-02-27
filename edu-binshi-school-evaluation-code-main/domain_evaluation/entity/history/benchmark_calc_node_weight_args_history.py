from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, Numeric, String


class BenchmarkCalcNodeWeightArgsHistoryEntity(HistoryEntity):
    __tablename__ = "st_benchmark_calc_node_weight_args_history"
    __table_args__ = {"comment": "计算方式为权重时的计算参数（历史）"}

    benchmark_calc_node_id = Column(String(40), nullable=False, comment="计算节点的id", index=True)
    weight = Column(Numeric, nullable=False, comment="权重")
    seq = Column(Integer, nullable=False, comment="排序码")


Index(
    "idx_benchmark_calc_node_weight_args_history_time_range",
    BenchmarkCalcNodeWeightArgsHistoryEntity.id,
    BenchmarkCalcNodeWeightArgsHistoryEntity.begin_at,
    BenchmarkCalcNodeWeightArgsHistoryEntity.end_at.desc(),
    unique=True,
)
