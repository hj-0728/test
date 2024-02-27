from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ObservationCreatorScopeHistoryEntity(HistoryEntity):
    """
    观测创建者范围历史
    """

    __tablename__ = "st_observation_creator_scope_history"
    __table_args__ = {"comment": "观测创建者范围历史"}
    observation_creator_id = Column(String(40), comment="观测创建者id", nullable=False)
    scope_res_category = Column(String(255), comment="范围资源类别", nullable=False)
    scope_res_id = Column(String(40), comment="范围资源id", nullable=False)


Index(
    "idx_observation_creator_scope_history_time_range",
    ObservationCreatorScopeHistoryEntity.id,
    ObservationCreatorScopeHistoryEntity.commenced_on,
    ObservationCreatorScopeHistoryEntity.ceased_on.desc(),
    unique=True,
)
