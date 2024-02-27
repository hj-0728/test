from infra_utility.base_plus_model import BasePlusModel


class PlanStatusCountVm(BasePlusModel):

    status: str
    count: int

