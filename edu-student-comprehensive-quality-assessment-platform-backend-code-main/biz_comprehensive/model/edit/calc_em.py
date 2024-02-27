from infra_basic.basic_model import VersionedModel
from infra_utility.base_plus_model import BasePlusModel


class SaveCalcAssignEditModel(VersionedModel):
    """
    保存 assign 类型计算规则
    """

    input_res_category: str
    input_res_id: str
    belongs_to_res_category: str
    belongs_to_res_id: str
    score: int


class SaveCalcRuleAssignEditModel(VersionedModel):
    """
    保存 assign 类型计算规则
    """

    belongs_to_res_category: str
    belongs_to_res_id: str
    score: int


class CalcResourceEditModel(BasePlusModel):
    """
    计算资源
    """

    clue_res_id: str  # 线索id
    clue_res_category: str  # 线索类型
    input_res_category: str
    input_res_id: str
    owner_res_category: str  # 所有者类型 班级/学生,DIMENSION_DEPT_TREE/ESTABLISHMENT_ASSIGN
    owner_res_id: str
