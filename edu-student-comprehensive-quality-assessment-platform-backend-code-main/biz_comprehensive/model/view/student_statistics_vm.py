from enum import Enum
from typing import Optional

from infra_basic.basic_model import BasePlusModel
from infra_basic.errors import BusinessError
from pydantic import root_validator


class EnumRankingRange(Enum):
    TOP_30 = "领航者"
    TOP_30_70 = "建设者"
    TOP_70_100 = "启航者"


class StudentStatisticsViewModel(BasePlusModel):
    total_points: int
    total_bright_spot: int
    ranking_range: Optional[str]
    percentage: float

    @root_validator
    def validate_ranking_range(cls, values):
        percentage = values.get("percentage")
        if percentage is None:
            return values
        if not (0 <= percentage <= 100):
            raise BusinessError("排名范围必须在0-100之间")
        if 0 <= percentage <= 30:
            values["ranking_range"] = EnumRankingRange.TOP_30.value
        elif 30 < percentage <= 70:
            values["ranking_range"] = EnumRankingRange.TOP_30_70.value
        else:
            values["ranking_range"] = EnumRankingRange.TOP_70_100.value
        return values
