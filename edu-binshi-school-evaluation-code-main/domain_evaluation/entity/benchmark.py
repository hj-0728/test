from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Index, String, text
from sqlalchemy.dialects.postgresql import JSONB

from domain_evaluation.entity.history.benchmark_history import BenchmarkHistoryEntity


class BenchmarkEntity(VersionedEntity):
    """
    基准
    """

    __tablename__ = "st_benchmark"
    __table_args__ = {"comment": "基准"}
    __history_entity__ = BenchmarkHistoryEntity
    indicator_id = Column(String(40), comment="评价指标id", nullable=False, index=True)
    name = Column(String(255), comment="名称", nullable=False)
    guidance = Column(String(500), comment="指南", nullable=True)
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束时间（默认infinity，如果被删加上时间）",
        server_default=text("'infinity'::timestamptz"),
    )
    benchmark_strategy_id = Column(
        String(40), comment="基准策略id(给页面参考的需要填写的东西)", nullable=False, index=True
    )
    benchmark_strategy_params = Column(JSONB, comment="页面输入的内容", nullable=True)


Index(
    "idx_benchmark_start_finish_time_range",
    BenchmarkEntity.id,
    BenchmarkEntity.start_at,
    BenchmarkEntity.finish_at.desc(),
    unique=True,
)


Index(
    "ix_st_benchmark_indicator_and_start_finish_time",
    BenchmarkEntity.indicator_id,
    BenchmarkEntity.start_at,
    BenchmarkEntity.finish_at.desc(),
    unique=True,
)
