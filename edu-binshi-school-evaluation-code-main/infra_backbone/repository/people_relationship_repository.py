from typing import List, Optional

from infra_basic.basic_repository import BasicRepository

# from infra_basic.transaction import Transaction
from sqlalchemy.engine import Transaction

from infra_backbone.entity.people_relationship import PeopleRelationshipEntity
from infra_backbone.model.people_relationship_model import PeopleRelationshipModel


class PeopleRelationshipRepository(BasicRepository):
    def insert_people_relationship(
        self, data: PeopleRelationshipModel, transaction: Transaction
    ) -> str:
        """
        添加人与人的关系
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=PeopleRelationshipEntity, entity_model=data, transaction=transaction
        )

    def delete_people_relationship(self, people_relationship_id: str, transaction: Transaction):
        """
        添加人与人的关系
        :param people_relationship_id:
        :param transaction:
        :return:
        """
        return self._delete_versioned_entity_by_id(
            entity_cls=PeopleRelationshipEntity,
            entity_id=people_relationship_id,
            transaction=transaction,
        )

    def update_people_relationship(
        self,
        data: PeopleRelationshipModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新用户人员信息
        :param data:
        :param transaction:
        :param limited_col_list:
        :return:
        """

        return self._update_versioned_entity_by_model(
            entity_cls=PeopleRelationshipEntity,
            update_model=data,
            limited_col_list=limited_col_list,
            transaction=transaction,
        )

    def get_people_relationship_list(self, people_id: str):
        """
        获取人员的关系列表
        """
        sql = """
        select * from st_people_relationship
        where subject_people_id = :people_id and start_at <= now() and finish_at > now()
        """
        return self._fetch_all_to_model(
            model_cls=PeopleRelationshipModel, sql=sql, params={"people_id": people_id}
        )
