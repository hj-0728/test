from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String, Text

from biz_comprehensive.entity.history.observation_point_history import ObservationPointHistoryEntity


class ObservationPointEntity(VersionedEntity):
    """
    观测点
    """

    __tablename__ = "st_observation_point"
    __table_args__ = {"comment": "观测点 "}
    __history_entity__ = ObservationPointHistoryEntity
    name = Column(String(255), comment="观测点名称", nullable=False)
    code = Column(Text, comment="编码", nullable=True)
    category = Column(String(255), comment="观测点类型（表扬和批评）", nullable=False)
