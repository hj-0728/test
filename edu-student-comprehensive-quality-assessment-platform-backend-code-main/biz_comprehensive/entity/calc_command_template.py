from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.calc_command_template_history import (
    CalcCommandTemplateHistoryEntity,
)


class CalcCommandTemplateEntity(VersionedEntity):
    """
    计算命令模板
    """

    __tablename__ = "st_calc_command_template"
    __table_args__ = {"comment": "计算命令模板"}
    __history_entity__ = CalcCommandTemplateHistoryEntity
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
