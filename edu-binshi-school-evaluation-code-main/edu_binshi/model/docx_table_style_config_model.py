from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumReportStyleCode(Enum):
    """
    word表格样式 code
    """

    TITLE = "标题"
    CLASS = "班级"
    NAME = "姓名"
    COMMON = "常规文本"
    COMMON_CENTER = "常规文本居中"
    COMMON_BOLD = "常规加粗"
    COMMON_BOLD_CENTER = "常规加粗居中"
    COMMON_REF_BOLD_CENTER = "常规加粗居中红色"


class DocxTableStyleConfigModel(VersionedModel):
    """
    word表格样式配置
    """

    name: str
    code: str
    belong_style_template_file_name: str
    row: int
    col: int
