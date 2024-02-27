from typing import List, Optional

from infra_basic.basic_model import VersionedModel


class ObservationPointViewModel(VersionedModel):
    """
    观测点列表
    """

    name: str
    category: str
    category_name: Optional[str]
    point_score: Optional[int]
    file_id: Optional[str]
    file_url: Optional[str]
    scene_id_list: Optional[List[str]]


class ObservationPointListViewModel(VersionedModel):
    """
    观测点列表
    """

    commend_obs_point_list: List[ObservationPointViewModel]
    to_be_improved_obs_point_list: List[ObservationPointViewModel]


class ObservationPointSystemIconViewModel(VersionedModel):
    """
    观测点列表
    """

    commend_obs_point_list: List[ObservationPointViewModel]
    to_be_improved_obs_point_list: List[ObservationPointViewModel]


class SceneObservationPointViewModel(VersionedModel):
    """
    场景观测点列表
    """

    name: str
    category: str
    category_name: Optional[str]
    file_id: Optional[str]
    file_url: Optional[str]
    point_score: int
