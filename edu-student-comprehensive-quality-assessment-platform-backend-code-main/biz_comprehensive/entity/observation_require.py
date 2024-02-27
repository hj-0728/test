from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String

from biz_comprehensive.entity.history.observation_require_history import (
    ObservationRequireHistoryEntity,
)


class ObservationRequireEntity(VersionedEntity):
    """
    观测需求
    """

    __tablename__ = "st_observation_require"
    __table_args__ = {"comment": "观测需求"}
    __history_entity__ = ObservationRequireHistoryEntity
    observation_batch_id = Column(String(40), comment="观测批次id", nullable=False)
    expected_perform_res_category = Column(
        String(255), comment="预期执行资源类别（例如 PARENTS_OF_STUDENT/ESTABLISHMENT_ASSIGN）", nullable=False
    )
    expected_perform_res_id = Column(
        String(40), comment="预期执行资源id（学生people_id/编制分配id）", nullable=False
    )
    observee_res_category = Column(String(255), comment="被观察者类别，编制分配的id", nullable=False)
    observee_res_id = Column(String(40), comment="被观察者id", nullable=False)
    required_res_category = Column(
        String(255), comment="被要求的资源类型（可以是TODO_BATCH/ASSESSMENT）", nullable=False
    )
    required_res_id = Column(String(40), comment="要求资源id", nullable=False)
