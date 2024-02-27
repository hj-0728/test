from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Numeric, String


class BenchmarkCalcNodeRangeValueArgsHistoryEntity(HistoryEntity):
    __tablename__ = "st_benchmark_calc_node_range_value_args_history"
    __table_args__ = {"comment": "计算方式为区间取值时的计算参数（历史）"}

    benchmark_calc_node_id = Column(String(40), nullable=False, comment="计算节点的id", index=True)
    min_score = Column(Numeric, nullable=False, comment="最小分")
    max_score = Column(Numeric, nullable=False, comment="最大分")
    left_operator = Column(String(255), nullable=False, comment="操作符的列表")
    right_operator = Column(String(255), nullable=False, comment="操作符的列表")
    match_value = Column(String(255), nullable=False, comment="匹配到的值")


Index(
    "idx_benchmark_calc_node_range_value_args_history_time_range",
    BenchmarkCalcNodeRangeValueArgsHistoryEntity.id,
    BenchmarkCalcNodeRangeValueArgsHistoryEntity.begin_at,
    BenchmarkCalcNodeRangeValueArgsHistoryEntity.end_at.desc(),
    unique=True,
)
