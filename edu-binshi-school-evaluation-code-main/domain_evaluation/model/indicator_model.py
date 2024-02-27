from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel


class IndicatorModel(VersionedModel):
    """
    指标
    """

    name: str
    seq: Optional[int]
    comments: Optional[str]
    start_at: datetime
    finish_at: datetime
    is_activated: bool = True
