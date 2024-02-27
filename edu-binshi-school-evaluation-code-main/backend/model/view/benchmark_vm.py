from typing import Optional, List

from infra_basic.basic_model import BasicModel


class BenchmarkVm(BasicModel):
    """
    基准
    """

    indicator_id: str
    name: Optional[str]
    guidance: Optional[str]
    score_symbol_name: str
    value_type: str
    string_options: Optional[List[str]]
