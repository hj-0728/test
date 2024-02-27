from typing import Any, Dict, List, Optional

from infra_basic.basic_model import VersionedModel


class CalcResultViewModel(VersionedModel):
    """
    计算结果
    """

    owner_res_category: str  # 所有者类型 班级/学生,DIMENSION_DEPT_TREE/ESTABLISHMENT_ASSIGN
    owner_res_id: str
    calc_result: Optional[Any]


class FuncCalcResultLogViewModel(VersionedModel):
    """
    方法计算结果
    """

    func: Optional[str]
    func_args: Optional[Dict[str, Any]]
    calc_result: Optional[List[CalcResultViewModel]]
