from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Numeric, String, Text


class TodoResultHistoryEntity(HistoryEntity):
    """
    代办事项结果历史
    """

    __tablename__ = "st_todo_result_history"
    __table_args__ = {"comment": "代办事项结果历史"}
    todo_id = Column(String(40), comment="代办事项id（EXAM/QUIZ/HOMEWORK）", nullable=False)
    establishment_assign_id = Column(String(40), comment="编制分配id", nullable=False)
    result_string_value = Column(String(255), comment="结果字符串值", nullable=True)
    result_numeric_value = Column(Numeric, comment="结果数值值", nullable=True)
    status = Column(String(255), comment="状态（READY/SUBMITTED/CONFIRMED）", nullable=False)
    comment = Column(Text, comment="备注", nullable=True)


Index(
    "idx_todo_result_history_time_range",
    TodoResultHistoryEntity.id,
    TodoResultHistoryEntity.commenced_on,
    TodoResultHistoryEntity.ceased_on.desc(),
    unique=True,
)
