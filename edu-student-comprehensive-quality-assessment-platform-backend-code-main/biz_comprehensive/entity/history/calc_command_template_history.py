from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class CalcCommandTemplateHistoryEntity(HistoryEntity):
    """
    计算命令模板历史
    """

    __tablename__ = "st_calc_command_template_history"
    __table_args__ = {"comment": "计算命令模板历史"}
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)


Index(
    "idx_calc_command_template_history_time_range",
    CalcCommandTemplateHistoryEntity.id,
    CalcCommandTemplateHistoryEntity.commenced_on,
    CalcCommandTemplateHistoryEntity.ceased_on.desc(),
    unique=True,
)
