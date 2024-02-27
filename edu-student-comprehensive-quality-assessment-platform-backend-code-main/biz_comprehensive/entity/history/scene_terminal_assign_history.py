from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class SceneTerminalAssignHistoryEntity(HistoryEntity):
    """
    场景终端分配历史
    """

    __tablename__ = "st_scene_terminal_assign_history"
    __table_args__ = {"comment": "菜单历史"}
    scene_id = Column(String(40), comment="场景id", nullable=False, index=True)
    terminal_category = Column(
        String(255),
        comment="CLASS_PC（TEACHER_MOBILE, PARENT_MOBILE, CLASS_PC/TEACHER_MOBILE/PARENT_MOBILE/CLASS_BOARD/CLASS_PAD）",
        nullable=False,
    )


Index(
    "idx_scene_terminal_assign_history_time_range",
    SceneTerminalAssignHistoryEntity.id,
    SceneTerminalAssignHistoryEntity.commenced_on,
    SceneTerminalAssignHistoryEntity.ceased_on.desc(),
    unique=True,
)
