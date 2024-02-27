"""
钉钉部门
"""

from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_dingtalk.entity.dingtalk_dept import DingtalkDeptEntity
from infra_dingtalk.model.dingtalk_dept_model import DingtalkDeptModel


class DingtalkDeptRepository(BasicRepository):
    """
    钉钉部门
    """

    def fetch_corp_dingtalk_dept_list(
        self,
        dingtalk_corp_id: str,
    ) -> List[DingtalkDeptModel]:
        """
        获取组织内钉钉的部门列表
        """

        sql = """select swd.*,
        coalesce(swd2.remote_dept_id, 0::varchar) as parent_remote_dept_id
        from st_dingtalk_dept swd
        left join st_dingtalk_dept swd2 on swd.parent_dingtalk_dept_id = swd2.id
        where swd.dingtalk_corp_id = :dingtalk_corp_id"""
        return self._fetch_all_to_model(
            model_cls=DingtalkDeptModel,
            sql=sql,
            params={"dingtalk_corp_id": dingtalk_corp_id},
        )

    def insert_dingtalk_dept(self, dept: DingtalkDeptModel, transaction: Transaction) -> str:
        """
        插入钉钉部门
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DingtalkDeptEntity, entity_model=dept, transaction=transaction
        )

    def update_dingtalk_dept(self, dept: DingtalkDeptModel, transaction: Transaction):
        """
        更新钉钉部门
        """

        return self._update_versioned_entity_by_model(
            entity_cls=DingtalkDeptEntity, update_model=dept, transaction=transaction
        )

    def delete_dingtalk_dept(self, dingtalk_dept_id: str, transaction: Transaction):
        """
        删除钉钉部门
        """
        self._delete_versioned_entity_by_id(
            entity_cls=DingtalkDeptEntity,
            entity_id=dingtalk_dept_id,
            transaction=transaction,
        )

    def get_dingtalk_dept_by_corp_id(self, dingtalk_corp_id: str) -> List[DingtalkDeptModel]:
        """
        获取所有的钉钉k12部门
        :param dingtalk_corp_id:
        :return:
        """

        sql = """
        select * from st_dingtalk_dept where dingtalk_corp_id=:dingtalk_corp_id
        """

        return self._fetch_all_to_model(
            model_cls=DingtalkDeptModel, sql=sql, params={"dingtalk_corp_id": dingtalk_corp_id}
        )
