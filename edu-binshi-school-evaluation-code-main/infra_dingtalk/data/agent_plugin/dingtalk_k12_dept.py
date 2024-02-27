"""
家校通讯录k12部门
"""

from typing import Dict, List, Optional

from infra_basic.basic_model import BasePlusModel
from pydantic import Field

from infra_dingtalk.data.agent_plugin.dingtalk_k12_dept_admin import DingtalkK12DeptAdmin
from infra_dingtalk.model.dingtalk_k12_dept_model import (
    DingtalkK12DeptModel,
)


class DingtalkK12Dept(BasePlusModel):
    """
    家校通讯录k12部门
    """

    dept_id: int
    dept_type: str
    name: str
    parent_id: Optional[int] = Field(alias="parentid")
    feature: Optional[str]
    nick: Optional[str]
    contact_type: str
    department_admins: List[DingtalkK12DeptAdmin] = []

    def to_dingtalk_k12_dept_em(
        self,
        dingtalk_corp_id: str,
        parent_remote_dept_id: int,
        parent_dingtalk_dept_id: str,
    ) -> DingtalkK12DeptModel:
        return DingtalkK12DeptModel(
            remote_dept_id=str(self.dept_id),
            name=self.name,
            dingtalk_corp_id=dingtalk_corp_id,
            parent_remote_dept_id=parent_remote_dept_id,
            parent_dingtalk_k12_dept_id=parent_dingtalk_dept_id,
            feature=self.feature,
            nick=self.nick,
            dept_type=self.dept_type.upper(),
            contact_type=self.contact_type,
        )

    def unique_dict(self) -> Dict:
        """
        获取用于判断唯一性的字典，用于判断数据是否改变
        """
        return {
            "dept_type": self.dept_type.upper(),
            "name": self.name,
            "parent_id": self.parent_id,
            "contact_type": self.contact_type,
            "nick": self.nick,
            "feature": self.feature,
        }
