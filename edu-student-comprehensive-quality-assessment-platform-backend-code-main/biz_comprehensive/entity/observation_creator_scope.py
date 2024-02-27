from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.observation_creator_scope_history import (
    ObservationCreatorScopeHistoryEntity,
)


class ObservationCreatorScopeEntity(VersionedEntity):
    """
    观察创建者范围
    """

    __tablename__ = "st_observation_creator_scope"
    __table_args__ = {"comment": "观察创建者范围"}
    __history_entity__ = ObservationCreatorScopeHistoryEntity
    observation_creator_id = Column(String(40), comment="观测创建者id", nullable=False)
    scope_res_category = Column(String(255), comment="范围资源类别", nullable=False)
    scope_res_id = Column(String(40), comment="范围资源id", nullable=False)
