from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.postgresql import JSONB


class ObservationCategoryHistoryEntity(HistoryEntity):
    """
    观察分类历史
    """

    __tablename__ = "st_observation_category_history"
    __table_args__ = {"comment": "观察分类历史"}
    name = Column(String(255), comment="分类名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    init_mechanism_func = Column(String(255), comment="初始化机制函数", nullable=True)
    init_mechanism_args = Column(JSONB, comment="初始化机制参数", nullable=True)


Index(
    "idx_observation_category_history_time_range",
    ObservationCategoryHistoryEntity.id,
    ObservationCategoryHistoryEntity.commenced_on,
    ObservationCategoryHistoryEntity.ceased_on.desc(),
    unique=True,
)
