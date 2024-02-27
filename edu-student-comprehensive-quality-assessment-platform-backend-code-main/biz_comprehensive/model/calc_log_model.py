from datetime import datetime
from typing import Any, Dict, List, Optional

from infra_basic.basic_model import VersionedModel

from biz_comprehensive.model.view.calc_result_vm import CalcResultViewModel


class CalcLogModel(VersionedModel):
    """
    计算日志
    """

    calc_rule_id: str
    calc_on: datetime
    pre_func: Optional[str]
    pre_func_args: Optional[Dict[str, Any]]
    calc_func: Optional[str]
    calc_func_args: Optional[Dict[str, Any]]
    post_func: Optional[str]
    post_func_args: Optional[Dict[str, Any]]
    calc_result: Optional[Dict[str, Optional[List[CalcResultViewModel]]]]
