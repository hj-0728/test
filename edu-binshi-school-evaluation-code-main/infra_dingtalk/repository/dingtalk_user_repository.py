from typing import List, Optional

from infra_basic.basic_repository import (
    BasicRepository,
    OrderCondition,
    PageFilterParams,
    PageInitParams,
)
from infra_basic.transaction import Transaction

from infra_dingtalk.entity.dingtalk_user import DingtalkUserEntity
from infra_dingtalk.model.dingtalk_user_model import DingtalkUserModel


class DingtalkUserRepository(BasicRepository):
    """
    钉钉用户 repository
    """

    def get_dingtalk_user_by_id(self, user_id: str) -> Optional[DingtalkUserModel]:
        """
        通过表的id获取钉钉用户信息
        @param user_id:
        @return:
        """

        sql = """select * from st_dingtalk_user where id = :user_id"""
        return self._fetch_first_to_model(
            model_cls=DingtalkUserModel, sql=sql, params={"user_id": user_id}
        )

    def fetch_dingtalk_user_list_with_dept(
        self,
        dingtalk_corp_id: str,
    ) -> List[DingtalkUserModel]:
        """
        获取钉钉用户列表
        """

        sql = """select su.*, array_agg(json_build_object('remote_dept_id',
        sd.remote_dept_id, 'id', sdu.id, 'duty', sdu.duty,
        'version', sdu.version, 'seq', sdu.seq)) as dingtalk_dept_user_duty_list,
        array_agg(sd.remote_dept_id) as remote_dept_ids
        from st_dingtalk_user su
        inner join st_dingtalk_dept_user_duty sdu on su.id = sdu.dingtalk_user_id
        inner join st_dingtalk_dept sd on sdu.dingtalk_dept_id = sd.id
        where su.dingtalk_corp_id = :dingtalk_corp_id
        group by su.id"""
        return self._fetch_all_to_model(
            model_cls=DingtalkUserModel,
            sql=sql,
            params={"dingtalk_corp_id": dingtalk_corp_id},
        )

    def insert_dingtalk_user(self, user: DingtalkUserModel, transaction: Transaction) -> str:
        """
        插入钉钉用户
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DingtalkUserEntity, entity_model=user, transaction=transaction
        )

    def update_dingtalk_user(self, user: DingtalkUserModel, transaction: Transaction):
        """
        更新钉钉用户
        """
        self._update_versioned_entity_by_model(
            entity_cls=DingtalkUserEntity, update_model=user, transaction=transaction
        )

    def delete_dingtalk_user(self, dingtalk_user_id: str, transaction: Transaction):
        """
        删除钉钉用户
        """
        self._delete_versioned_entity_by_id(
            entity_cls=DingtalkUserEntity,
            entity_id=dingtalk_user_id,
            transaction=transaction,
        )

    def get_dingtalk_user_by_remote_user_id(
        self, dingtalk_corp_id: str, remote_user_id: str
    ) -> Optional[DingtalkUserModel]:
        """
        通过钉钉corp id跟远程用户id 获取钉钉用户信息
        @param dingtalk_corp_id:
        @param remote_user_id:
        @return:
        """

        sql = """select * from st_dingtalk_user where dingtalk_corp_id = :dingtalk_corp_id 
        and remote_user_id = :remote_user_id"""
        return self._fetch_first_to_model(
            model_cls=DingtalkUserModel,
            sql=sql,
            params={"dingtalk_corp_id": dingtalk_corp_id, "remote_user_id": remote_user_id},
        )

    def get_dingtalk_user_by_dingtalk_corp_id(
        self, query_params: PageFilterParams, dingtalk_corp_id: str
    ):
        """
        通过钉钉corp id 获取钉钉用户
        """
        sql = """
        select * from st_dingtalk_user swu
        where swu.dingtalk_corp_id = :dingtalk_corp_id and 
        not exists(select * from st_dingtalk_user_user_map swuum where swu.id = swuum.dingtalk_user_id)
        """
        page_init_params = PageInitParams(
            sql=sql,
            order_columns=[OrderCondition(column_name="name")],
            filter_columns=[
                "name",
            ],
            params={"dingtalk_corp_id": dingtalk_corp_id},
        )
        return self._paginate(
            result_type=DingtalkUserModel,
            total_params=page_init_params,
            page_params=query_params,
        )

    def get_dingtalk_user_by_name(self, name: str) -> Optional[DingtalkUserModel]:
        """
        通过钉钉corp id跟远程用户id 获取钉钉用户信息
        @param name:
        @return:
        """

        sql = """select * from st_dingtalk_user where name=:name"""
        return self._fetch_first_to_model(
            model_cls=DingtalkUserModel,
            sql=sql,
            params={
                "name": name,
            },
        )

    def get_all_dingtalk_user_without_people(self):
        sql = """
        SELECT wu.* FROM "st_dingtalk_user" wu 
        LEFT JOIN st_people_user pu on pu.user_id = wu.id
        left join st_people sp on sp.id = pu.people_id
        where pu.id is null
        """
        return self._fetch_all_to_model(model_cls=DingtalkUserModel, sql=sql, params={})

    def get_corp_all_dingtalk_user(self, dingtalk_corp_id: str) -> List[DingtalkUserModel]:
        """
        获取钉钉用户
        :param dingtalk_corp_id:
        :return:
        """

        sql = """
        with dept_duty_info as (
        select dingtalk_user_id, array_agg(json_build_object('dingtalk_dept_id',
        sdu.dingtalk_dept_id, 'id', sdu.id, 'duty', sdu.duty,
        'version', sdu.version, 'seq', sdu.seq)) as dingtalk_dept_user_duty_list
        from st_dingtalk_dept_user_duty sdu
        group by  dingtalk_user_id
        ),
        k12_dept_duty_info as (
        select dingtalk_user_id, array_agg(json_build_object('dingtalk_k12_dept_id',
        sdu.dingtalk_k12_dept_id, 'id', sdu.id, 'duty', sdu.duty,
        'version', sdu.version)) as dingtalk_k12_dept_user_duty_list
        from st_dingtalk_user_k12_dept_duty sdu
        group by  dingtalk_user_id
        )
        SELECT wu.*, ddi.dingtalk_dept_user_duty_list,
        coalesce(kddi.dingtalk_k12_dept_user_duty_list, array[]::json[]) as dingtalk_k12_dept_user_duty_list
        FROM st_dingtalk_user wu
        left join dept_duty_info ddi on wu.id = ddi.dingtalk_user_id
        left join k12_dept_duty_info kddi on wu.id = kddi.dingtalk_user_id
        where dingtalk_corp_id = :dingtalk_corp_id
        """

        return self._fetch_all_to_model(
            model_cls=DingtalkUserModel,
            sql=sql,
            params={
                "dingtalk_corp_id": dingtalk_corp_id,
            },
        )

    def get_dingtalk_user_by_ids(self, dingtalk_user_ids: List[str]) -> List[DingtalkUserModel]:
        """
        通过钉钉用户id列表获取钉钉用户信息
        @param dingtalk_user_ids:
        @return:
        """

        sql = """ select * from st_dingtalk_user where id =any(:dingtalk_user_ids) """
        return self._fetch_all_to_model(
            model_cls=DingtalkUserModel,
            sql=sql,
            params={"dingtalk_user_ids": dingtalk_user_ids},
        )

    def get_dingtalk_user_by_people_id(self, people_id: str) -> Optional[DingtalkUserModel]:
        """
        通过人员id获取钉钉用户信息
        :param people_id:
        :return:
        """
        sql = """
        select swu.* from st_dingtalk_user swu 
        join st_people_user spu on swu.id = spu.user_id and spu.user_category = 'dingtalk_USER'
        where spu.people_id = :people_id
        """
        return self._fetch_first_to_model(
            model_cls=DingtalkUserModel,
            sql=sql,
            params={"people_id": people_id},
        )
