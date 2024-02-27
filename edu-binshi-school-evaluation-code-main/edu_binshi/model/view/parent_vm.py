from typing import Optional

from infra_utility.base_plus_model import BasePlusModel


class ParentVm(BasePlusModel):
    """
    家长视图模型
    """

    id: str
    name: str

    phone_detail: Optional[str]
