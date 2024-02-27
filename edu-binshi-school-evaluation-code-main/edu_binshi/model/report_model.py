from enum import Enum
from typing import List, Optional

from infra_utility.algorithm.tree import TreeNodeModel
from infra_utility.base_plus_model import BasePlusModel

from edu_binshi.model.docx_table_style_config_model import EnumReportStyleCode


class ScoreSymbolForReportModel(BasePlusModel):
    name: str
    code: str
    value_type: str
    numeric_precision: Optional[int]
    string_options: Optional[List[str]]
    is_activated: bool = True
    icon_bucket_name: str
    icon_object_name: str
    numeric_max_score: Optional[float]
    numeric_min_score: Optional[float]


class ReportBenchmarkScoreModel(BasePlusModel):
    numeric_score: Optional[float]
    string_score: Optional[str]
    score_symbol: ScoreSymbolForReportModel


class ReportBenchmarkTagModel(BasePlusModel):
    score_symbol_list: List[ScoreSymbolForReportModel] = []
    indicator_id: str
    benchmark_tag_name: str
    benchmark_tag_id: str
    benchmark_tag_seq: int
    benchmark_score_list: List[ReportBenchmarkScoreModel]


class ReportIndicatorTreeModel(TreeNodeModel):
    evaluation_criteria_tree_tag_id: str
    evaluation_criteria_tree_tag_name: str
    indicator_id: str
    indicator_name: str
    parent_indicator_id: Optional[str]
    seq: int
    seq_list: List[int]
    path_list: List[str]
    benchmark_tag_list: List[ReportBenchmarkTagModel]
    benchmark_row_count: int = 0
    benchmark_score_count: int = 0
    current_col: int = 0
    score_symbol_list_agg: List[List[ScoreSymbolForReportModel]] = []


class GrowthRecordReportEstablishmentAssignModel(BasePlusModel):
    evaluation_criteria_tree_tag_name: str
    evaluation_criteria_tree_tag_seq: str
    indicator_tree_list: List[ReportIndicatorTreeModel]


class GrowthRecordReportEstablishmentAssignInfoModel(BasePlusModel):
    title: str
    dept_name: str
    people_name: str
    period_name: str
    evaluation_criteria_plan_name: str
    dimension_dept_tree_id: str
    footer_text: Optional[str]


class EnumJavaAsposeWordsLineStyle(Enum):
    """
    java aspose.words的线条样式枚举
    """

    NONE = 0
    SINGLE = 1
    THICK = 2
    DOUBLE = 3
    HAIRLINE = 5
    DOT = 6
    DASH_LARGE_GAP = 7
    DOT_DASH = 8
    DOT_DOT_DASH = 9
    TRIPLE = 10
    THIN_THICK_SMALL_GAP = 11
    THICK_THIN_SMALL_GAP = 12
    THIN_THICK_THIN_SMALL_GAP = 13
    THIN_THICK_MEDIUM_GAP = 14
    THICK_THIN_MEDIUM_GAP = 15
    THIN_THICK_THIN_MEDIUM_GAP = 16
    THIN_THICK_LARGE_GAP = 17
    THICK_THIN_LARGE_GAP = 18
    THIN_THICK_THIN_LARGE_GAP = 19
    WAVE = 20
    DOUBLE_WAVE = 21
    DASH_SMALL_GAP = 22
    DASH_DOT_STROKER = 23
    EMBOSS_3_D = 24
    ENGRAVE_3_D = 25
    OUTSET = 26
    INSET = 27


class EnumReportCategory(Enum):
    """
    报告类型枚举
    """

    GROWTH_RECORD = "道德与法治善行撑场记录表"
    GOOD_CONDUCT_EVALUATION_RECORD = "12345蔚蓝善行准则评价表"


class CellPositionModel(BasePlusModel):
    row: int
    col: int


class BorderStyleCellPositionModel(CellPositionModel):
    top: int = EnumJavaAsposeWordsLineStyle.NONE.value
    bottom: int = EnumJavaAsposeWordsLineStyle.NONE.value
    right: int = EnumJavaAsposeWordsLineStyle.NONE.value
    left: int = EnumJavaAsposeWordsLineStyle.NONE.value


class CellDataModel(BasePlusModel):
    row: int
    col: int
    value: Optional[str]
    type: Optional[str] = "string"
    style: str = EnumReportStyleCode.COMMON.name


class MergeCellModel(BasePlusModel):
    start: CellPositionModel
    end: CellPositionModel
