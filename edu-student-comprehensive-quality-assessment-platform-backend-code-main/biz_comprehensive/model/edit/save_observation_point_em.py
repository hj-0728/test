from typing import List, Optional

from infra_basic.basic_model import VersionedModel


class SaveObservationPointEditModel(VersionedModel):
    """
    观测点
    """

    name: str
    code: Optional[str]
    category: str
    point_score: Optional[int]  # 观测点的分数
    file_id: str
    scene_id_list: Optional[List[str]]
