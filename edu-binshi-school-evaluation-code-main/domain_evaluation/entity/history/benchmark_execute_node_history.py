from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, String


class BenchmarkExecuteNodeHistoryEntity(HistoryEntity):
    __tablename__ = "st_benchmark_execute_node_history"
    __table_args__ = {"comment": "基准的执行节点（历史）"}

    benchmark_id = Column(String(40), nullable=False, comment="基准id", index=True)
    name = Column(String(255), nullable=False, comment="名称")
    category = Column(String(255), nullable=False, comment="类型（input、calc）")
    next_node_id = Column(String(40), nullable=True, comment="下一节点id")
    seq = Column(Integer, nullable=False, comment="排序码")


Index(
    "idx_benchmark_execute_node_history_time_range",
    BenchmarkExecuteNodeHistoryEntity.id,
    BenchmarkExecuteNodeHistoryEntity.begin_at,
    BenchmarkExecuteNodeHistoryEntity.end_at.desc(),
    unique=True,
)
