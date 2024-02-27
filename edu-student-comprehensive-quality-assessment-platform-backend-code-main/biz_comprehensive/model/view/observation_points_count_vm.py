from infra_basic.basic_model import BasePlusModel


class ObservationPointsCountViewModel(BasePlusModel):
    category: str
    points: int
