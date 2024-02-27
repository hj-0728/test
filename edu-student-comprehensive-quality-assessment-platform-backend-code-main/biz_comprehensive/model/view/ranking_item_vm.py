from typing import Optional

from infra_basic.basic_model import BasePlusModel


class RankingItemViewModel(BasePlusModel):
    """
    排行榜项
    """

    id: str
    establishment_assign_id: str
    name: str
    points: int
    avatar: Optional[str]
    seq: Optional[int]
