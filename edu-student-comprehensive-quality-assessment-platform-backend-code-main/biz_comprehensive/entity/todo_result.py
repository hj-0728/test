from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Numeric, String, Text

from biz_comprehensive.entity.history.todo_result_history import TodoResultHistoryEntity


class TodoResultEntity(VersionedEntity):
    """
    待办结果
    """

    __tablename__ = "st_todo_result"
    __table_args__ = {"comment": "待办结果"}
    __history_entity__ = TodoResultHistoryEntity
    todo_id = Column(String(40), comment="代办事项id（EXAM/QUIZ/HOMEWORK）", nullable=False)
    establishment_assign_id = Column(String(40), comment="编制分配id", nullable=False)
    result_string_value = Column(String(255), comment="结果字符串值", nullable=True)
    result_numeric_value = Column(Numeric, comment="结果数值值", nullable=True)
    status = Column(String(255), comment="状态（READY/SUBMITTED/CONFIRMED）", nullable=False)
    comment = Column(Text, comment="备注", nullable=True)
