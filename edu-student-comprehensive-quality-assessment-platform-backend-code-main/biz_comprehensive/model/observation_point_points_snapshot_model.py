from datetime import datetime
from typing import List

from infra_basic.basic_model import VersionedModel


class ObservationPointPointsSnapshotModel(VersionedModel):
    """
    观测点积分快照
    """

    dimension_dept_tree_id: str
    observation_action_id: str
    observation_action_performer_name: str
    observation_on: datetime
    observation_point_log_id: str
    observee_name: str
    observation_point_name: str
    observation_point_category: str
    observation_point_icon: str
    scene_ids: List[str]
    points_log_id: str
    owner_res_category: str
    owner_res_id: str
    owner_name: str
    owner_avatar: str
    gained_points: float
    symbol_code: str
    numeric_precision: int
    belongs_to_period_id: str
