from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB


class BenchmarkWrapperMethodHistoryEntity(HistoryEntity):
    __tablename__ = "st_benchmark_wrapper_method_history"
    __table_args__ = {"comment": "基准的包装计算函数"}

    benchmark_id = Column(String(40), nullable=False, comment="基准的id", index=True)
    wrapper_scope = Column(String(255), nullable=False, comment="包裹范围（before/after，前置/后置）")
    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=True, comment="编码")
    method_name = Column(String(255), nullable=False, comment="执行函数名")
    method_args = Column(JSONB, nullable=True, comment="执行参数")
    seq = Column(Integer, nullable=False, comment="执行序号")


Index(
    "idx_benchmark_wrapper_method_history_time_range",
    BenchmarkWrapperMethodHistoryEntity.id,
    BenchmarkWrapperMethodHistoryEntity.begin_at,
    BenchmarkWrapperMethodHistoryEntity.end_at.desc(),
    unique=True,
)
