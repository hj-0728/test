from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class TodoItemSubjectAssignHistoryEntity(HistoryEntity):
    """
    待办事项科目分配历史
    """

    __tablename__ = "st_todo_item_subject_assign_history"
    __table_args__ = {"comment": "待办事项科目分配历史"}
    todo_item_id = Column(String(40), comment="待办事项id", nullable=False)
    subject_id = Column(String(40), comment="科目id", nullable=False)


Index(
    "idx_todo_item_subject_assign_history_time_range",
    TodoItemSubjectAssignHistoryEntity.id,
    TodoItemSubjectAssignHistoryEntity.commenced_on,
    TodoItemSubjectAssignHistoryEntity.ceased_on.desc(),
    unique=True,
)
