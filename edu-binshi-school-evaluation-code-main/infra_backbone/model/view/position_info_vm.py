"""
职位
"""

from typing import Optional

from infra_basic.basic_model import BasicModel


class PositionVm(BasicModel):
    """
    职位
    """

    name: Optional[str]
    code: Optional[str]
