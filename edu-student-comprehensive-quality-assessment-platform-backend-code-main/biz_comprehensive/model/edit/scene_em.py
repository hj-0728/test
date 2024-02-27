from typing import List, Optional

from infra_basic.basic_model import BasePlusModel


class SceneEditModel(BasePlusModel):
    """
    场景编辑
    """

    id: Optional[str]
    version: Optional[int] = 1
    name: str
    code: Optional[str]
    terminal_category_list: List[str]
    observation_point_id_list: List[str] = []
