from infra_basic.basic_model import BasePlusModel
from infra_basic.query_params import PageFilterParams


class TeacherObservationQueryParams(BasePlusModel):
    started_on: str
    ended_on: str
    period_id: str
    people_id: str


class TeacherObservationPageFilterParams(PageFilterParams):
    dimension_dept_tree_id: str
    started_on: str
    ended_on: str
    period_id: str
