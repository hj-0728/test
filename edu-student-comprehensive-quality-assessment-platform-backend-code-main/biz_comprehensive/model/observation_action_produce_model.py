from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumObservationActionProduceResCategory(Enum):
    """
    观察动作的产出资源类型
    """

    OBSERVATION_POINT_LOG = "观测点日志"
    CREATIONS = "作品"
    MOMENTS = "点滴"
    TODO_RESULT = "待办结果"
    ASSESSMENT_RESULT = "评估结果"


class ObservationActionProduceModel(VersionedModel):
    """
    观察动作的产出
    """

    observation_action_id: str
    produce_res_category: str
    produce_res_id: str
