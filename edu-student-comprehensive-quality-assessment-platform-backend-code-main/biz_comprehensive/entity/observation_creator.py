from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String

from biz_comprehensive.entity.history.observation_creator_history import (
    ObservationCreatorHistoryEntity,
)


class ObservationCreatorEntity(VersionedEntity):
    """
    观察创建者
    """

    __tablename__ = "st_observation_creator"
    __table_args__ = {"comment": "观察创建者"}
    __history_entity__ = ObservationCreatorHistoryEntity
    observation_category_id = Column(String(40), comment="观察者分类id", nullable=False)
    proposed_res_category = Column(String(255), comment="建议资源类型（发出提议的资源）", nullable=False)
    proposed_res_id = Column(String(40), comment="建议资源id", nullable=False)
    proposed_representative = Column(String(255), comment="代表（例如年级组，用户自己输入文本）", nullable=False)
    ended_on = Column(DateTime(timezone=True), comment="结束时间", nullable=True)
    demanded_category = Column(String(255), comment="需求类型（枚举，班主任/任课老师/家长）", nullable=False)
    status = Column(String(255), comment="状态（DRAFT/PUBLISNED/ABOLISHED/ARCHIVED）", nullable=False)
    required_res_category = Column(
        String(255), comment="需求资源类型（被要求的资源类型，可以是todo_batch或者assessment）", nullable=False
    )
    required_res_id = Column(String(40), comment="需求资源id", nullable=False)
