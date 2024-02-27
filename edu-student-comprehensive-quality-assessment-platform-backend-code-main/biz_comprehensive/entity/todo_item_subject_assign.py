from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.todo_item_subject_assign_history import (
    TodoItemSubjectAssignHistoryEntity,
)


class TodoItemSubjectAssignEntity(VersionedEntity):
    """
    待办事项科目分配
    """

    __tablename__ = "st_todo_item_subject_assign"
    __table_args__ = {"comment": "待办事项科目分配"}
    __history_entity__ = TodoItemSubjectAssignHistoryEntity
    todo_item_id = Column(String(40), comment="待办事项id", nullable=False)
    subject_id = Column(String(40), comment="科目id", nullable=False)
