from typing import List

from infra_basic.transaction import Transaction

from biz_comprehensive.model.scene_observation_point_assign_model import (
    SceneObservationPointAssignModel,
)
from biz_comprehensive.repository.scene_obeservation_point_assign_repository import (
    SceneObservationPointAssignRepository,
)


class SceneObservationPointAssignService:
    """
    场景观测点分配
    """

    def __init__(
        self,
        scene_observation_point_assign_repository: SceneObservationPointAssignRepository,
    ):
        self.__scene_observation_point_assign_repository = scene_observation_point_assign_repository

    def get_scene_observation_point_assign_list_by_scene_id(self, scene_id: str):
        """
        根据场景id获取场景观测点分配
        """
        return self.__scene_observation_point_assign_repository.get_scene_observation_point_assign_list_by_scene_id(
            scene_id=scene_id,
        )

    def get_scene_observation_point_assign_list_by_observation_point_id(
        self, observation_point_id: str
    ):
        """
        根据观测点id获取场景观测点分配
        """
        return self.__scene_observation_point_assign_repository.get_scene_observation_point_assign_list_by_observation_point_id(
            observation_point_id=observation_point_id,
        )

    def update_scene_observation_point_assign_with_scene_id(
        self,
        scene_id: str,
        observation_point_id_list: List[str],
        transaction: Transaction,
    ):
        """
        新增或修改场景观测点分配
        """
        scene_observation_point_assign_list = self.__scene_observation_point_assign_repository.get_scene_observation_point_assign_list_by_scene_id(
            scene_id=scene_id,
        )
        scene_observation_point_assign_dict = {
            scene_observation_point_assign.observation_point_id: scene_observation_point_assign
            for scene_observation_point_assign in scene_observation_point_assign_list
        }
        for observation_point_id in observation_point_id_list:
            if not scene_observation_point_assign_dict.get(observation_point_id):
                data = SceneObservationPointAssignModel(
                    scene_id=scene_id,
                    observation_point_id=observation_point_id,
                )
                self.__scene_observation_point_assign_repository.insert_scene_observation_point_assign(
                    data=data,
                    transaction=transaction,
                )
        for observation_point_id in scene_observation_point_assign_dict.keys():
            if observation_point_id not in observation_point_id_list:
                self.__scene_observation_point_assign_repository.delete_scene_observation_point_assign(
                    scene_observation_point_assign_id=scene_observation_point_assign_dict[
                        observation_point_id
                    ].id,
                    transaction=transaction,
                )

    def save_observation_point_scene(
        self,
        observation_point_id: str,
        scene_id_list: List[str],
        transaction: Transaction,
    ):
        """
        保存观测点的场景
        :param observation_point_id:
        :param scene_id_list:
        :param transaction:
        :return:
        """

        scene_observation_point_assign_list = self.__scene_observation_point_assign_repository.get_scene_observation_point_assign_list_by_observation_point_id(
            observation_point_id=observation_point_id,
        )

        scene_id_db_list = [x.scene_id for x in scene_observation_point_assign_list]

        need_add_scene_id_list = [x for x in scene_id_list if x not in scene_id_db_list]

        need_delete_assign_list = [
            x.id for x in scene_observation_point_assign_list if x.scene_id not in scene_id_list
        ]

        for assign_id in need_delete_assign_list:
            self.__scene_observation_point_assign_repository.delete_scene_observation_point_assign(
                scene_observation_point_assign_id=assign_id,
                transaction=transaction,
            )

        for scene_id in need_add_scene_id_list:
            self.__scene_observation_point_assign_repository.insert_scene_observation_point_assign(
                data=SceneObservationPointAssignModel(
                    scene_id=scene_id,
                    observation_point_id=observation_point_id,
                ),
                transaction=transaction,
            )
