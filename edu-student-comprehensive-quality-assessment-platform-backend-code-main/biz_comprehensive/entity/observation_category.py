from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB

from biz_comprehensive.entity.history.observation_category_history import (
    ObservationCategoryHistoryEntity,
)


class ObservationCategoryEntity(VersionedEntity):
    """
    观察分类
    """

    __tablename__ = "st_observation_category"
    __table_args__ = {"comment": "观察分类"}
    __history_entity__ = ObservationCategoryHistoryEntity
    name = Column(String(255), comment="分类名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    init_mechanism_func = Column(String(255), comment="初始化机制函数", nullable=True)
    init_mechanism_args = Column(JSONB, comment="初始化机制参数", nullable=True)
