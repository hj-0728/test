from enum import Enum
from typing import List, Optional

from infra_basic.basic_model import VersionedModel


class EnumScoreSymbolValueType(Enum):
    """
    得分符号值类型
    """

    NUM = "分值"
    STRING = "分级"


class ScoreSymbolModel(VersionedModel):
    """
    得分符号
    """

    name: str
    code: str
    value_type: str
    numeric_precision: Optional[int]
    string_options: Optional[List[str]]
    is_activated: bool = True


class ScoreSymbolNameVm(VersionedModel):
    """
    得分符号
    """

    # name: str
    value_type: str
    value_type_string: Optional[str]
    options_list: List[ScoreSymbolModel] = []
