from typing import List, Optional

from infra_basic.basic_repository import BasicRepository

# from infra_basic.transaction import Transaction
from sqlalchemy.engine import Transaction

from infra_backbone.entity.people_user import PeopleUserEntity
from infra_backbone.model.people_model import PeopleUserModel


class PeopleUserRepository(BasicRepository):
    def insert_people_user(self, data: PeopleUserModel, transaction: Transaction):
        self._insert_versioned_entity_by_model(
            entity_cls=PeopleUserEntity, entity_model=data, transaction=transaction
        )

    def update_people_user(
        self,
        data: PeopleUserModel,
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
            entity_cls=PeopleUserEntity,
            update_model=data,
            limited_col_list=limited_col_list,
            transaction=transaction,
        )

    def fetch_people_user_by_user_id(self, user_id: str) -> Optional[PeopleUserModel]:
        """
        通过用户id获取人员用户的关联
        :param user_id:
        :return:
        """

        sql = """select * from st_people_user where user_id = :user_id"""
        return self._fetch_first_to_model(
            model_cls=PeopleUserModel, sql=sql, params={"user_id": user_id}
        )

    def get_people_user_list_by_people_id_list(
        self, people_id_list: List[str]
    ) -> List[PeopleUserModel]:
        """
        通过人员id列表获取人员用户列表
        :param people_id_list:
        :return:
        """

        sql = """
        select * from st_people_user 
        where people_id = any(array[:people_id_list])
        """
        return self._fetch_all_to_model(
            model_cls=PeopleUserModel, sql=sql, params={"people_id_list": people_id_list}
        )
