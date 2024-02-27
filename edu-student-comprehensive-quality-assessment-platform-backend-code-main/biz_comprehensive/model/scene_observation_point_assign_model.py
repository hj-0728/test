from infra_basic.basic_model import VersionedModel


class SceneObservationPointAssignModel(VersionedModel):
    """
    场景观察点分配
    """

    scene_id: str
    observation_point_id: str
