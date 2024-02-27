from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumContextDeptMapResCategory(Enum):
    """
    上下文部门关联类型
    """

    DINGTALK_K12_DEPT = "钉钉k12部门"
    DINGTALK_DEPT = "钉钉部门"


class ContextDeptMapModel(VersionedModel):
    """
    上下文部门关联
    """

    dept_id: str
    res_category: str
    res_id: str
