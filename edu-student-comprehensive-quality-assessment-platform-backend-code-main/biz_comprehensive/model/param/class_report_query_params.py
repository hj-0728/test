from enum import Enum
from typing import Optional

from infra_basic.basic_model import BasePlusModel
from infra_basic.query_params import PageFilterParams


class EnumQueryCategory(str, Enum):
    TOP3_RANKING = "前3排行榜"


class ClassReportQueryParams(BasePlusModel):
    tree_id: str
    started_on: str
    ended_on: str
    period_id: str
    period_category: str

    category: Optional[str]


class ClassReportPageFilterParams(PageFilterParams):
    tree_id: str
    started_on: str
    ended_on: str
    period_id: str
    period_category: str
    performer_res_id: str
