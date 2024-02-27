from typing import List, Optional

from infra_basic.basic_model import VersionedModel


class BenchmarkScoreSymbolViewModel(VersionedModel):
    """
    基准得分符号
    """

    name: str
    code: str
    value_type: str
    numeric_precision: Optional[int]
    string_options: Optional[List[str]]
    is_activated: bool = True
    limited_string_options_str: Optional[str]
    limited_string_options: Optional[List[str]]
    numeric_max_score: Optional[float]
    numeric_min_score: Optional[float]
