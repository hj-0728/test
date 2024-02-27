from typing import Optional, Union

from infra_basic.basic_model import BasePlusModel


class CommandEditModel(BasePlusModel):
    """
    command
    """

    category: str
    args: Optional[Union[BasePlusModel, str]]
