from typing import Optional

from infra_basic.basic_model import VersionedModel


class CalcTriggerViewModel(VersionedModel):
    """
    计算触发器
    """

    calc_rule_id: str
    input_res_category: str
    input_res_id: str
    rule_can_be_deleted: Optional[bool]
