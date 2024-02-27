from typing import Dict, Optional

from infra_basic.basic_model import BasePlusModel

from infra_dingtalk.model.dingtalk_dept_model import DingtalkDeptModel


class DingtalkDept(BasePlusModel):
    """
    通讯录（内部通讯录）部门
    """

    dept_id: int
    name: str
    parent_id: int
    order: Optional[int]
    level: Optional[int]

    def to_dingtalk_dept_em(
        self,
        dingtalk_corp_id: str,
        parent_remote_dept_id: int,
        parent_dingtalk_dept_id: str,
    ):
        return DingtalkDeptModel(
            remote_dept_id=self.dept_id,
            name=self.name,
            seq=self.order,
            dingtalk_corp_id=dingtalk_corp_id,
            parent_remote_dept_id=parent_remote_dept_id,
            parent_dingtalk_dept_id=parent_dingtalk_dept_id,
        )

    def unique_dict(self) -> Dict:
        """
        获取用于判断唯一性的字典，用于判断数据是否改变
        """
        unique_cols = ["name", "parent_id", "order"]
        data = {}
        for key, value in self.dict().items():
            if key in unique_cols:
                data[key] = value
        return data
