"""
周期
"""

from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel


class PeriodModel(VersionedModel):
    """
    周期
    """

    period_category_id: str
    name: str
    code: Optional[str]
    started_on: datetime
    ended_on: datetime
    parent_id: Optional[str]
