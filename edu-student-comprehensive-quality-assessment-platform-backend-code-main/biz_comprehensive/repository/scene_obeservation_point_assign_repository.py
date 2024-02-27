from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.scene_observation_point_assign import (
    SceneObservationPointAssignEntity,
)
from biz_comprehensive.model.scene_observation_point_assign_model import (
    SceneObservationPointAssignModel,
)


class SceneObservationPointAssignRepository(BasicRepository):
    """
    场景观测点分配
    """

    def insert_scene_observation_point_assign(
        self, data: SceneObservationPointAssignModel, transaction: Transaction
    ) -> str:
        """
        新增场景观测点分配
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=SceneObservationPointAssignEntity,
            entity_model=data,
            transaction=transaction,
        )

    def update_scene_observation_point_assign(
        self, data: SceneObservationPointAssignModel, transaction: Transaction
    ):
        """
        修改场景观测点分配
        """
        return self._update_versioned_entity_by_model(
            entity_cls=SceneObservationPointAssignEntity,
            update_model=data,
            transaction=transaction,
        )

    def delete_scene_observation_point_assign(
        self, scene_observation_point_assign_id: str, transaction: Transaction
    ):
        """
        删除场景观测点分配
        """
        return self._delete_versioned_entity_by_id(
            entity_cls=SceneObservationPointAssignEntity,
            entity_id=scene_observation_point_assign_id,
            transaction=transaction,
        )

    def get_scene_observation_point_assign_list_by_scene_id(
        self, scene_id: str
    ) -> List[SceneObservationPointAssignModel]:
        """
        根据场景id获取场景观测点分配
        """
        sql = """
            select * from st_scene_observation_point_assign where scene_id = :scene_id
        """
        return self._fetch_all_to_model(
            model_cls=SceneObservationPointAssignModel,
            sql=sql,
            params={"scene_id": scene_id},
        )

    def get_scene_observation_point_assign_list_by_observation_point_id(
        self, observation_point_id: str
    ) -> List[SceneObservationPointAssignModel]:
        """
        根据观测点id获取场景观测点分配
        """
        sql = """
            select * from st_scene_observation_point_assign where observation_point_id = :observation_point_id
        """
        return self._fetch_all_to_model(
            model_cls=SceneObservationPointAssignModel,
            sql=sql,
            params={"observation_point_id": observation_point_id},
        )
