from typing import List, Optional

from infra_basic.basic_model import BasePlusModel


class ObservationPointStatisticVm(BasePlusModel):
    """
    场景观察点分配
    """

    category: str
    category_name: Optional[str]
    num: int


class SceneViewModel(BasePlusModel):
    """
    场景vm
    """

    id: str
    version: int
    name: str
    code: Optional[str]
    terminal_category_list: List[str] = []
    terminal_category_name_list: List[str] = []
    observation_point_statistics: List[ObservationPointStatisticVm] = []
