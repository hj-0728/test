from typing import Optional

from infra_utility.base_plus_model import BasePlusModel


class SceneStatisticsQueryParams(BasePlusModel):
    """
    场景统计 查询条件
    """

    observation_point_category: str
    people_id: Optional[str]
