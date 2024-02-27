from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.establishment_assign import EstablishmentAssignEntity
from infra_backbone.model.establishment_assign_model import EstablishmentAssignModel
from infra_backbone.model.view.establishment_assign_vm import EstablishmentAssignVm


class EstablishmentAssignRepository(BasicRepository):
    def insert_establishment_assign(
        self, data: EstablishmentAssignModel, transaction: Transaction
    ) -> str:
        """
        插入编制分配
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=EstablishmentAssignEntity, entity_model=data, transaction=transaction
        )

    def update_establishment_assign(
        self,
        data: EstablishmentAssignModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        插入编制分配
        :param data:
        :param transaction:
        :return:
        """
        return self._update_versioned_entity_by_model(
            entity_cls=EstablishmentAssignEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_establishment_assign_by_id(
        self, establishment_assign_id: str, transaction: Transaction
    ):
        """
        删除编制分配
        :param establishment_assign_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=EstablishmentAssignEntity,
            entity_id=establishment_assign_id,
            transaction=transaction,
        )

    def get_people_establishment_assign(self, organization_id: str, people_id: str):
        """
        获取人编制分配
        :param organization_id:
        :param people_id:
        :return:
        """
        sql = """
        select sea.*, sd1.category as dimension_category from st_establishment_assign sea
        join st_establishment se on sea.establishment_id = se.id
        join st_dimension_dept_tree sddt on se.dimension_dept_tree_id = sddt.id
        join st_dimension sd1 on sddt.dimension_id = sd1.id
        join st_dept sd on sddt.dept_id = sd.id
        where sd.organization_id = :organization_id and sea.people_id = :people_id
        and sea.start_at <=now() and sea.finish_at  > now()
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=EstablishmentAssignVm,
            params={
                "organization_id": organization_id,
                "people_id": people_id,
            },
        )

    def get_current_people_establishment_assign_by_establishment_assign_ids(
        self, establishment_assign_ids: List[str]
    ) -> List[EstablishmentAssignModel]:
        """
        获取当前激活的人的根据 establishment_assign_ids
        :param establishment_assign_ids:
        :return:
        """

        sql = """
        select ea.* 
        from st_establishment_assign ea INNER JOIN st_people p on ea.people_id=p.id
        where ea.id=any(array[:establishment_assign_ids]) and p.is_available=true
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=EstablishmentAssignModel,
            params={
                "establishment_assign_ids": establishment_assign_ids,
            },
        )
