from enum import Enum
from typing import List, Optional

from infra_basic.basic_model import VersionedModel


class EnumSymbolCode(Enum):
    """
    符号值类型
    """

    POINTS = "积分"
    BRIGHT_SPOT = "闪光点"
    STAR = "星星"
    MOON = "月亮"
    SUN = "太阳"
    CROWN = "王冠"


class EnumSymbolValueType(Enum):
    """
    符号值类型
    """

    NUM = "分值"
    STRING = "分级"


class EnumSymbolCategory(Enum):
    POINTS = "积分"
    BRIGHT_SPOT = "闪光点"
    RATING_SHOW = "等级展示"  # 星星、月亮、太阳、王冠（等级也需要换算）
    SCORE = "得分"


class SymbolModel(VersionedModel):
    """
    符号
    """

    name: str
    code: Optional[str]
    value_type: str
    numeric_precision: Optional[int]
    string_options: Optional[List[str]]
    is_activated: bool = True
    category: str
