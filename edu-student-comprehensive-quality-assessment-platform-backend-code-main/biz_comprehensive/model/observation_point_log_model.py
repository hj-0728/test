from datetime import datetime
from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumObserveeResCategory(str, Enum):
    ESTABLISHMENT_ASSIGN = "编制分配"
    DIMENSION_DEPT_TREE = "维度部门树"


class ObservationPointLogModel(VersionedModel):
    observation_point_id: str
    observee_res_category: str
    observee_res_id: str
    started_on: Optional[datetime]
    ended_on: Optional[datetime]
    comment: Optional[str]
