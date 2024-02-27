from typing import Optional, List

from infra_utility.base_plus_model import BasePlusModel


class BenchmarkInputNodeVm(BasePlusModel):
    benchmark_id: str
    benchmark_name: str
    benchmark_source_category: str
    numeric_min_score: Optional[float]
    numeric_max_score: Optional[float]
    filler_calc_method: Optional[str]
    limited_string_options: Optional[List[str]]
    score_symbol_name: str
    score_symbol_code: str
    score_symbol_value_type: Optional[str]
    score_symbol_numeric_precision: Optional[int]
    score_symbol_string_options: Optional[List[str]]
    score_result: Optional[str]
    string_score: Optional[str]
    numeric_score: Optional[float]
    input_score_log_id: Optional[str]
    input_score_log_version: Optional[int]
    display_popover: bool = False
    can_view: bool = False
