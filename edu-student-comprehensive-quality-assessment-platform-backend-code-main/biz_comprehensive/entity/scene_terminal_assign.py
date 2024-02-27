from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.scene_terminal_assign_history import (
    SceneTerminalAssignHistoryEntity,
)


class SceneTerminalAssignEntity(VersionedEntity):
    """
    场景终端分配
    """

    __tablename__ = "st_scene_terminal_assign"
    __table_args__ = {"comment": "菜单 "}
    __history_entity__ = SceneTerminalAssignHistoryEntity
    scene_id = Column(String(40), comment="场景id", nullable=False, index=True)
    terminal_category = Column(
        String(255),
        comment="终端类型（CLASS_PC，TEACHER_MOBILE, PARENT_MOBILE, CLASS_PC/TEACHER_MOBILE/PARENT_MOBILE/CLASS_BOARD/CLASS_PAD）",
        nullable=False,
    )
