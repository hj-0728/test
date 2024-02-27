from enum import Enum


class EnumScoreSymbolCode(Enum):
    STAR = "星"
    GRADE = "等级"


class EnumFileRelationshipRelationship(Enum):
    REPORT_PDF = "报告(PEF格式)"
    REPORT_WORD = "报告(DOCX格式)"
    REPORT_ZIP = "报告(ZIP格式)"


class EnumFileRelationshipResCategory(Enum):

    REPORT_RECORD = "报告记录"
    EVALUATION_ASSIGNMENT = "评价分配"
