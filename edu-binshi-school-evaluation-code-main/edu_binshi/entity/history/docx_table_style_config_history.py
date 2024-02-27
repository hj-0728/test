from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String, Integer


class DocxTableStyleConfigHistoryEntity(HistoryEntity):
    """
    word表格样式配置（历史实体类）
    """

    __tablename__ = "st_docx_table_style_config_history"
    __table_args__ = {"comment": "word表格样式配置（历史）"}
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=False)
    belong_style_template_file_name = Column(String(255), comment="归属于哪个样式模板文件", nullable=False)
    row = Column(Integer, comment="样式在样式模板文件table中的行号", nullable=False)
    col = Column(Integer, comment="样式在样式模板文件table中的列号", nullable=False)


Index(
    "idx_docx_table_style_config_history_time_range",
    DocxTableStyleConfigHistoryEntity.id,
    DocxTableStyleConfigHistoryEntity.begin_at,
    DocxTableStyleConfigHistoryEntity.end_at.desc(),
    unique=True,
)
