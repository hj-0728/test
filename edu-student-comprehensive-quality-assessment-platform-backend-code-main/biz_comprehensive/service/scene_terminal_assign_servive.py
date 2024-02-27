from typing import List

from infra_basic.transaction import Transaction

from biz_comprehensive.model.scene_terminal_assign_model import SceneTerminalAssignModel
from biz_comprehensive.repository.scene_terminal_assign_repository import (
    SceneTerminalAssignRepository,
)


class SceneTerminalAssignService:
    """
    场景终端分配
    """

    def __init__(self, scene_terminal_assign_repository: SceneTerminalAssignRepository):
        self.__scene_terminal_assign_repository = scene_terminal_assign_repository

    def get_scene_terminal_assign_list_by_scene_id(self, scene_id: str):
        """
        根据场景id获取场景终端分配
        """
        return self.__scene_terminal_assign_repository.get_scene_terminal_assign_list_by_scene_id(
            scene_id=scene_id,
        )

    def update_scene_terminal_assign_with_scene_id(
        self, scene_id: str, terminal_category_list: List[str], transaction: Transaction
    ):
        """
        新增或修改场景终端分配
        """
        scene_terminal_assign_list = (
            self.__scene_terminal_assign_repository.get_scene_terminal_assign_list_by_scene_id(
                scene_id=scene_id,
            )
        )
        scene_terminal_assign_dict = {
            scene_terminal_assign.terminal_category: scene_terminal_assign
            for scene_terminal_assign in scene_terminal_assign_list
        }
        for terminal_category in terminal_category_list:
            if not scene_terminal_assign_dict.get(terminal_category):
                data = SceneTerminalAssignModel(
                    scene_id=scene_id,
                    terminal_category=terminal_category,
                )
                self.__scene_terminal_assign_repository.insert_scene_terminal_assign(
                    data=data,
                    transaction=transaction,
                )
        for terminal_category in scene_terminal_assign_dict.keys():
            if terminal_category not in terminal_category_list:
                self.__scene_terminal_assign_repository.delete_scene_terminal_assign(
                    scene_terminal_assign_id=scene_terminal_assign_dict[terminal_category].id,
                    transaction=transaction,
                )
