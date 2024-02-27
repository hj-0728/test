"""
command
"""
from infra_basic.basic_model import BasePlusModel
from typing import Optional


class CommandEm(BasePlusModel):
    """
    command
    """

    category: str
    args: Optional[BasePlusModel]
