from infra_utility.base_plus_model import BasePlusModel


class SceneObservationPointQueryParams(BasePlusModel):
    """
    场景观测点 查询条件
    """

    scene_id: str
    observation_point_category: str
