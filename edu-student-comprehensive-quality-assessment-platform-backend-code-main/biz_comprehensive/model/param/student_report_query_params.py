from infra_basic.basic_model import BasePlusModel
from infra_basic.query_params import PageFilterParams


class StudentReportQueryParams(BasePlusModel):
    establishment_assign_id: str
    started_on: str
    ended_on: str
    period_id: str


class StudentReportPageFilterParams(PageFilterParams):
    establishment_assign_id: str
    started_on: str
    ended_on: str
    period_id: str
    scene_id: str
