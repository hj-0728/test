from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ObservationPointHistoryEntity(HistoryEntity):
    """
    观测点历史
    """

    __tablename__ = "st_observation_point_history"
    __table_args__ = {"comment": "观测点历史"}
    name = Column(String(255), comment="观测点名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    category = Column(String(255), comment="观测点类型（表扬和批评）", nullable=False)


Index(
    "idx_observation_point_history_time_range",
    ObservationPointHistoryEntity.id,
    ObservationPointHistoryEntity.commenced_on,
    ObservationPointHistoryEntity.ceased_on.desc(),
    unique=True,
)
