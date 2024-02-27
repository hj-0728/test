from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.capacity import CapacityEntity
from infra_backbone.model.capacity_model import CapacityModel
from infra_backbone.model.view.capacity_vm import CapacityVm


class CapacityRepository(BasicRepository):
    def insert_capacity(self, data: CapacityModel, transaction: Transaction) -> str:
        """
        插入capacity
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=CapacityEntity, entity_model=data, transaction=transaction
        )

    def delete_capacity_by_id(self, capacity_id: str, transaction: Transaction):
        """
        删除capacity
        :param capacity_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=CapacityEntity,
            entity_id=capacity_id,
            transaction=transaction,
        )

    def get_capacity_model_by_code(self, capacity_code: str) -> Optional[CapacityModel]:
        """
        获取capacity
        :param capacity_code:
        :return:
        """
        sql = """
        select * from st_capacity where code = :capacity_code
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=CapacityModel,
            params={"capacity_code": capacity_code},
        )

    def get_k12_capacity_list_by_dingtalk_user_id(self, dingtalk_user_id: str):
        """
        根据钉钉userid获取对应的capacity信息
        """
        sql = """
        select distinct sc.* from st_capacity sc
        join st_establishment se on sc.id = se.capacity_id and se.ended_on >= now()
        join st_dimension_dept_tree sddt on se.dimension_dept_tree_id = sddt.id
        join st_dimension sd on sddt.dimension_id = sd.id
        join st_establishment_assign sea on se.id = sea.establishment_id and sea.ended_on >= now()
        join st_context_people_user_map scum on sea.people_id = scum.people_id
        where scum.res_id = :dingtalk_user_id and scum.res_category = 'DINGTALK_USER' and sd.category = 'EDU'
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=CapacityVm,
            params={"dingtalk_user_id": dingtalk_user_id},
        )
