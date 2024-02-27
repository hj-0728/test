from typing import List

from infra_basic.basic_model import BasePlusModel

from biz_comprehensive.model.observation_action_produce_model import ObservationActionProduceModel


class ObservationActionWithProduceViewModel(BasePlusModel):
    id: str
    produce_list: List[ObservationActionProduceModel]
