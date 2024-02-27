from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ObservationActionProduceHistoryEntity(HistoryEntity):
    """
    观测动作产出历史
    """

    __tablename__ = "st_observation_action_produce_history"
    __table_args__ = {"comment": "观测动作产出历史"}
    observation_action_id = Column(String(40), comment="观测动作id", nullable=False)
    produce_res_category = Column(
        String(255),
        comment="产出资源类别（OBSERVATION_POINT_LOG/CREATIONS/MOMENTS/TODO_RESULT/ASSESSMENT_RESULT）",
        nullable=False,
    )
    produce_res_id = Column(String(40), comment="产出资源id", nullable=False)


Index(
    "idx_observation_action_produce_history_time_range",
    ObservationActionProduceHistoryEntity.id,
    ObservationActionProduceHistoryEntity.commenced_on,
    ObservationActionProduceHistoryEntity.ceased_on.desc(),
    unique=True,
)


Index(
    "idx_observation_action_produce_history_produce_res",
    ObservationActionProduceHistoryEntity.produce_res_category,
    ObservationActionProduceHistoryEntity.produce_res_id,
)
