"""
同步部门的服务
"""

from typing import Dict, Optional

from infra_basic.errors.input import DataNotFoundError
from infra_basic.transaction import Transaction

from infra_dingtalk.data.agent_plugin.dingtalk_dept import DingtalkDept
from infra_dingtalk.model.dingtalk_dept_model import DingtalkDeptModel
from infra_dingtalk.repository.dingtalk_dept_repository import DingtalkDeptRepository


class SyncDeptService:
    def __init__(self, dingtalk_dept_repository: DingtalkDeptRepository):
        self._dingtalk_dept_repository = dingtalk_dept_repository

    def sync_dingtalk_dept_from_remote(
        self,
        remote_dept_dict: Dict[int, DingtalkDept],
        dingtalk_corp_id: str,
        transaction: Transaction,
    ) -> Dict[int, DingtalkDeptModel]:
        """
        远程的部门和数据库的部门进行比较
        """
        db_dept_dict = self.get_dingtalk_dept_remote_id_dict(dingtalk_corp_id=dingtalk_corp_id)

        for remote_dept_id, remote_dept in remote_dept_dict.items():

            def __get_db_parent_dept_id() -> Optional[str]:
                if remote_dept_id == 1:
                    return None
                _parent = db_dept_dict.get(remote_dept.parent_id, None)
                if not _parent:
                    raise DataNotFoundError(f"{remote_dept_id}的父级部门")
                return _parent.id

            db_dept = db_dept_dict.get(remote_dept_id)
            if not db_dept:
                new_db_dept = remote_dept.to_dingtalk_dept_em(
                    dingtalk_corp_id=dingtalk_corp_id,
                    parent_dingtalk_dept_id=__get_db_parent_dept_id(),
                    parent_remote_dept_id=remote_dept.parent_id,
                )
                new_db_dept.id = self._dingtalk_dept_repository.insert_dingtalk_dept(
                    dept=new_db_dept, transaction=transaction
                )
                db_dept_dict[new_db_dept.remote_dept_id] = new_db_dept
            elif db_dept.unique_dict() != remote_dept.unique_dict():
                db_dept.parent_dingtalk_dept_id = __get_db_parent_dept_id()
                db_dept.parent_remote_dept_id = remote_dept.parent_id
                db_dept.seq = remote_dept.order
                db_dept.name = remote_dept.name
                self._dingtalk_dept_repository.update_dingtalk_dept(
                    dept=db_dept, transaction=transaction
                )

        for db_remote_dept_id, db_dept in db_dept_dict.items():
            if db_remote_dept_id not in remote_dept_dict:
                self._dingtalk_dept_repository.delete_dingtalk_dept(
                    dingtalk_dept_id=db_dept.id, transaction=transaction
                )
        return db_dept_dict

    def get_dingtalk_dept_remote_id_dict(
        self,
        dingtalk_corp_id: str,
    ) -> Dict[int, DingtalkDeptModel]:
        """
        获取钉钉部门以远程id为键，DingtalkDeptModel实例为值的字典
        """
        db_dept_list = self._dingtalk_dept_repository.fetch_corp_dingtalk_dept_list(
            dingtalk_corp_id=dingtalk_corp_id
        )
        return {x.remote_dept_id: x for x in db_dept_list}
