from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String, Integer

from edu_binshi.entity.history.docx_table_style_config_history import DocxTableStyleConfigHistoryEntity


class DocxTableStyleConfigEntity(VersionedEntity):
    """
    word表格样式配置
    """

    __tablename__ = "st_docx_table_style_config"
    __table_args__ = {"comment": "word表格样式配置"}
    __history_entity__ = DocxTableStyleConfigHistoryEntity
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=False)
    belong_style_template_file_name = Column(String(255), comment="归属于哪个样式模板文件", nullable=False)
    row = Column(Integer, comment="样式在样式模板文件table中的行号", nullable=False)
    col = Column(Integer, comment="样式在样式模板文件table中的列号", nullable=False)
