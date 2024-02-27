from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class BenchmarkCalcNodeHistoryEntity(HistoryEntity):
    __tablename__ = "st_benchmark_calc_node_history"
    __table_args__ = {"comment": "计算节点（历史）"}

    benchmark_execute_node_id = Column(String(40), nullable=False, comment="节点id", index=True)
    input_score_symbol_id = Column(String(40), nullable=False, comment="输入的符号id")
    output_score_symbol_id = Column(String(40), nullable=False, comment="输出的符号id")
    calc_method = Column(String(255), nullable=False, comment="计算方法（统计类的、权重类的、区间取值的）")


Index(
    "idx_benchmark_calc_node_history_time_range",
    BenchmarkCalcNodeHistoryEntity.id,
    BenchmarkCalcNodeHistoryEntity.begin_at,
    BenchmarkCalcNodeHistoryEntity.end_at.desc(),
    unique=True,
)
