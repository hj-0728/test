from enum import Enum
from typing import Optional, Tuple

from docx.enum.base import EnumValue
from infra_basic.basic_model import BasePlusModel


class EnumReportStyle(Enum):
    TAG_CELL = "标签"
    VERTICALLY_TAG_CELL = "纵向的标签"
    EVALUATION_CONTENT_CELL = "评价内容"
    ROOT_INDICATOR_CELL = "根指标"
    SCORE_CELL = "得分"


class ReportTableCellData(BasePlusModel):
    value: str
    root_score_cell: bool = False
    style: Optional[str]


class ReportCellStyle(BasePlusModel):
    font_size: float = 10.5
    color: Tuple = (0, 0, 0)
    bold: bool = False
    alignment: Optional[EnumValue]
