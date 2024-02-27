from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_dingtalk.entity.dingtalk_k12_parent import DingtalkK12ParentEntity
from infra_dingtalk.model.dingtalk_k12_parent_model import DingtalkK12ParentModel
from infra_dingtalk.model.view.dingtalk_k12_parent_vm import DingtalkK12ParentViewModel


class DingtalkK12ParentRepository(BasicRepository):
    """
    企微k12家长 repository
    """

    def get_dingtalk_k12_parent_by_id(
        self,
        k12_parent_id: str,
    ) -> Optional[DingtalkK12ParentModel]:
        """
        通过表的id获取企微k12家长信息
        @param k12_parent_id:
        @return:
        """

        sql = """select * from st_dingtalk_k12_parent where id = :id"""
        return self._fetch_first_to_model(
            model_cls=DingtalkK12ParentModel,
            sql=sql,
            params={"id": k12_parent_id},
        )

    def get_dingtalk_k12_parent_by_remote_user_id(
        self, dingtalk_corp_id: str, remote_user_id: str
    ) -> Optional[DingtalkK12ParentModel]:
        """
        通过企微corp id跟远程用户id 获取企微k12家长信息
        @param dingtalk_corp_id:
        @param remote_user_id:
        @return:
        """

        sql = """select * from st_dingtalk_k12_parent where dingtalk_corp_id = :dingtalk_corp_id 
        and remote_user_id = :remote_user_id"""
        return self._fetch_first_to_model(
            model_cls=DingtalkK12ParentModel,
            sql=sql,
            params={"dingtalk_corp_id": dingtalk_corp_id, "remote_user_id": remote_user_id},
        )

    def insert_dingtalk_k12_parent(
        self, parent: DingtalkK12ParentModel, transaction: Transaction
    ) -> str:
        """
        插入钉钉k12的家长
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DingtalkK12ParentEntity,
            entity_model=parent,
            transaction=transaction,
        )

    def update_dingtalk_k12_parent(self, parent: DingtalkK12ParentModel, transaction: Transaction):
        """
        更新钉钉k12的家长
        """

        self._update_versioned_entity_by_model(
            entity_cls=DingtalkK12ParentEntity,
            update_model=parent,
            transaction=transaction,
        )

    def delete_dingtalk_k12_parent(self, parent_id: str, transaction: Transaction):
        """
        删除钉钉k12的家长
        """

        self._delete_versioned_entity_by_id(
            entity_cls=DingtalkK12ParentEntity,
            entity_id=parent_id,
            transaction=transaction,
        )

    def get_dingtalk_k12_parent_by_corp_id(
        self, dingtalk_corp_id: str
    ) -> List[DingtalkK12ParentViewModel]:
        """
        通过企微corp id 获取企微k12家长信息
        @param dingtalk_corp_id:
        @return:
        """

        sql = """
        select kp.id,kp.remote_user_id,kp.unionid,kp.dingtalk_corp_id,kp.mobile,
        string_agg(ks.name||'-'||fr.relationship_name, '、' ORDER BY ks.name) as name
        from st_dingtalk_k12_parent kp 
        INNER JOIN st_dingtalk_k12_family_relationship fr on fr.dingtalk_k12_parent_id=kp.id 
        INNER JOIN st_dingtalk_k12_student ks on ks.id=fr.dingtalk_k12_student_id
        where kp.dingtalk_corp_id =:dingtalk_corp_id
        GROUP BY kp.id,kp.remote_user_id,kp.unionid,kp.dingtalk_corp_id,kp.mobile
        """
        return self._fetch_all_to_model(
            model_cls=DingtalkK12ParentViewModel,
            sql=sql,
            params={"dingtalk_corp_id": dingtalk_corp_id},
        )
