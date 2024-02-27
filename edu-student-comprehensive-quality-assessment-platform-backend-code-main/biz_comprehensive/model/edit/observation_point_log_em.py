from datetime import datetime
from typing import List, Optional

from infra_basic.basic_resource import BasicResource
from infra_utility.base_plus_model import BasePlusModel


class SaveObservationPointLogEditModel(BasePlusModel):
    """
    保存观测点日志
    """

    observation_point_id: str
    observee_res: BasicResource
    started_on: Optional[datetime]
    ended_on: Optional[datetime]
    comment: Optional[str]
    file_id_list: Optional[List[str]]
