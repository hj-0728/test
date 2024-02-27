from typing import List, Optional

from infra_basic.basic_model import BasePlusModel

from infra_backbone.model.view.capacity_vm import CapacityVm


class DingtalkUserForMobileVm(BasePlusModel):
    """
    手机端 钉钉用户vm
    """

    id: str
    name: Optional[str]
    user_category: str
    dingtalk_corp_id: str
    capacity_list: List[CapacityVm] = []
    current_capacity: CapacityVm
