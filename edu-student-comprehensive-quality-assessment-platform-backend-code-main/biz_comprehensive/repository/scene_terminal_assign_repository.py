from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.scene_terminal_assign import SceneTerminalAssignEntity
from biz_comprehensive.model.scene_terminal_assign_model import SceneTerminalAssignModel


class SceneTerminalAssignRepository(BasicRepository):
    """
    场景终端分配
    """

    def insert_scene_terminal_assign(
        self, data: SceneTerminalAssignModel, transaction: Transaction
    ) -> str:
        """
        新增场景终端分配
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=SceneTerminalAssignEntity,
            entity_model=data,
            transaction=transaction,
        )

    def update_scene_terminal_assign(
        self, data: SceneTerminalAssignModel, transaction: Transaction
    ):
        """
        修改场景终端分配
        """
        return self._update_versioned_entity_by_model(
            entity_cls=SceneTerminalAssignEntity,
            update_model=data,
            transaction=transaction,
        )

    def delete_scene_terminal_assign(self, scene_terminal_assign_id: str, transaction: Transaction):
        """
        删除场景终端分配
        """
        return self._delete_versioned_entity_by_id(
            entity_cls=SceneTerminalAssignEntity,
            entity_id=scene_terminal_assign_id,
            transaction=transaction,
        )

    def get_scene_terminal_assign_list_by_scene_id(
        self, scene_id: str
    ) -> List[SceneTerminalAssignModel]:
        """
        根据场景id获取场景终端分配
        """
        sql = """
        select * from st_scene_terminal_assign where scene_id = :scene_id
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=SceneTerminalAssignModel,
            params={"scene_id": scene_id},
        )
