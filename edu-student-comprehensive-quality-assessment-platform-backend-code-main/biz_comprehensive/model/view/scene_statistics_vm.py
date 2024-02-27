from typing import Optional

from infra_utility.base_plus_model import BasePlusModel


class SceneStatisticVm(BasePlusModel):
    """
    场景统计数据
    """

    id: Optional[str]
    name: str
    commend_obs_point_count: int
    to_be_improved_obs_point_count: int
