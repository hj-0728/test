from datetime import datetime
from typing import List, Optional

from infra_basic.basic_model import BasePlusModel


class ObservationPointPoints(BasePlusModel):
    owner_res_category: str
    owner_res_id: str
    owner_name: str
    gained_points: float
    symbol_code: str
    numeric_precision: int
    belongs_to_period_id: str
    owner_bucket_name: Optional[str]
    owner_object_name: Optional[str]


class ObservationPointPointsSnapshotViewModel(BasePlusModel):
    """
    观测点积分快照
    """

    dimension_dept_tree_id: str
    observation_action_id: str
    observation_action_performer_name: str
    observation_on: datetime
    observee_res_category: str
    observee_res_id: str
    observee_name: str
    observation_point_name: str
    observation_point_category: str
    observation_point_bucket_name: Optional[str]
    observation_point_object_name: Optional[str]

    points_list: List[ObservationPointPoints]
