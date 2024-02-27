from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumSceneTerminalCategory(Enum):
    """
    场景的category
    """

    CLASS_PC = "班级pc端"
    TEACHER_MOBILE = "教师手机端"
    PARENT_MOBILE = "家长手机端"
    CLASS_BOARD = "班级电子白板端"
    CLASS_PAD = "班级pad端"


class SceneTerminalAssignModel(VersionedModel):
    """
    场景终端分配
    """

    scene_id: str
    terminal_category: str
