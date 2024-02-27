from datetime import datetime
from typing import List, Optional

from infra_utility.base_plus_model import BasePlusModel
from infra_utility.datetime_helper import local_now
from pydantic import Field


class SaveObsActionEditModel(BasePlusModel):
    """
    保存观测行为
    """

    observation_require_id: Optional[str]
    performer_res_category: Optional[str]
    performer_res_id: Optional[str]
    performed_started_on: Optional[str] = Field(default_factory=local_now)
    performed_ended_on: Optional[str] = Field(default_factory=local_now)


class EvaluationObservationPointEditModel(BasePlusModel):
    observation_point_id: str
    amount: int


class SaveEvaluationObsActionEditModel(SaveObsActionEditModel):
    """
    保存评价的观测行为
    """

    observation_point_info: List[EvaluationObservationPointEditModel]
    observee_dept_tree_id_list: Optional[List[str]]
    observee_establishment_assign_id_list: Optional[List[str]]
    started_on: Optional[datetime] = Field(default_factory=local_now)
    ended_on: Optional[datetime] = Field(default_factory=local_now)
    comment: Optional[str]
    file_id_list: Optional[List[str]]
