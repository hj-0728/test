from typing import List, Optional

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.enum_helper import enum_to_dict_list, get_enum_value_by_name

from biz_comprehensive.data.constant import SceneConst
from biz_comprehensive.model.edit.scene_em import SceneEditModel
from biz_comprehensive.model.observation_point_model import EnumObservationPointCategory
from biz_comprehensive.model.scene_model import SceneModel
from biz_comprehensive.model.scene_terminal_assign_model import EnumSceneTerminalCategory
from biz_comprehensive.model.view.scene_statistics_vm import SceneStatisticVm
from biz_comprehensive.model.view.scene_vm import SceneViewModel
from biz_comprehensive.repository.scene_repository import SceneRepository
from biz_comprehensive.service.scene_observation_point_assign_service import (
    SceneObservationPointAssignService,
)
from biz_comprehensive.service.scene_terminal_assign_servive import SceneTerminalAssignService


class SceneService:
    """
    场景
    """

    def __init__(
        self,
        scene_repository: SceneRepository,
        scene_terminal_assign_service: SceneTerminalAssignService,
        scene_observation_point_assign_service: SceneObservationPointAssignService,
    ):
        self.__scene_repository = scene_repository
        self.__scene_terminal_assign_service = scene_terminal_assign_service
        self.__scene_observation_point_assign_service = scene_observation_point_assign_service

    def get_scene_list(self) -> List[SceneViewModel]:
        """
        获取场景列表
        """
        scene_list = self.__scene_repository.get_scene_list()
        for scene in scene_list:
            terminal_category_name_list = []
            for terminal_category in scene.terminal_category_list:
                terminal_category_name_list.append(
                    get_enum_value_by_name(
                        enum_class=EnumSceneTerminalCategory,
                        enum_name=terminal_category,
                    )
                )
            scene.terminal_category_name_list = terminal_category_name_list
            for observation_point in scene.observation_point_statistics:
                observation_point.category_name = get_enum_value_by_name(
                    enum_class=EnumObservationPointCategory,
                    enum_name=observation_point.category,
                )
        return scene_list

    def add_or_update_scene(self, scene_em: SceneEditModel, transaction: Transaction) -> str:
        """
        新增或修改场景
        :param scene_em:
        :param transaction:
        :return:
        """
        existed_scene = self.__scene_repository.get_scene_by_name(
            name=scene_em.name, scene_id=scene_em.id
        )
        if existed_scene:
            raise BusinessError("已存在相同场景名称")
        if scene_em.id:
            scene_id = scene_em.id
            self.__scene_repository.update_scene(
                data=scene_em.cast_to(SceneModel),
                transaction=transaction,
            )
        else:
            scene_id = self.__scene_repository.insert_scene(
                data=scene_em.cast_to(SceneModel),
                transaction=transaction,
            )
        self.__scene_terminal_assign_service.update_scene_terminal_assign_with_scene_id(
            scene_id=scene_id,
            terminal_category_list=scene_em.terminal_category_list,
            transaction=transaction,
        )
        self.__scene_observation_point_assign_service.update_scene_observation_point_assign_with_scene_id(
            scene_id=scene_id,
            observation_point_id_list=scene_em.observation_point_id_list,
            transaction=transaction,
        )
        return scene_id

    def delete_scene_by_scene_id(self, scene_id: str, transaction: Transaction):
        """
        删除scene
        :param scene_id:
        :param transaction:
        :return:
        """
        scene = self.__scene_repository.get_scene_model_by_scene_id(scene_id=scene_id)
        if not scene:
            raise BusinessError("未找到对应的场景")
        return self.__scene_repository.delete_scene(scene_id=scene_id, transaction=transaction)

    @staticmethod
    def get_scene_terminal_category_list():
        """
        获取终端列表
        :return:
        """
        return enum_to_dict_list(
            enum_class=EnumSceneTerminalCategory,
            name_col="value",
            value_col="label",
        )

    def get_scene_info_by_scene_id(self, scene_id: str) -> Optional[SceneEditModel]:
        """
        根据场景id获取场景信息
        :param scene_id:
        :return:
        """
        scene = self.__scene_repository.get_scene_model_by_scene_id(scene_id=scene_id)
        if not scene:
            raise BusinessError("未找到对应的场景")
        return scene

    def get_scene_with_observation_point_count(self, people_id: str, terminal: str) -> List[SceneStatisticVm]:
        """
        获取场景列表带有观测点数量
        :param people_id:
        :param terminal:
        :return:
        """
        scene_list = []
        default_scene_list = self.__scene_repository.get_scene_with_observation_point_count(terminal=terminal)
        if len(default_scene_list) == 0:
            raise BusinessError("未找到场景数据，清联系管理员")
        used_scene = self.__scene_repository.get_used_scene_with_observation_point_count(
            people_id=people_id, terminal=terminal
        )
        if used_scene and used_scene.commend_obs_point_count + used_scene.to_be_improved_obs_point_count > 0:
            used_scene.id = SceneConst.USED_SCENE
            scene_list.append(used_scene)
        scene_list.extend(default_scene_list)
        return scene_list
