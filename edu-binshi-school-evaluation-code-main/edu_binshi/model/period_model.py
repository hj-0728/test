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
    start_at: Optional[datetime]
    finish_at: Optional[datetime]
    parent_id: Optional[str]

    category_code: Optional[str]
    category_name: Optional[str]
