"""
钉钉部门
"""

from typing import Dict, Optional

from infra_basic.basic_model import VersionedModel


class DingtalkDeptModel(VersionedModel):
    """
    钉钉部门
    """

    dingtalk_corp_id: str
    remote_dept_id: int
    name: str
    parent_dingtalk_dept_id: Optional[str]
    parent_remote_dept_id: Optional[int]
    seq: int

    def unique_dict(self) -> Dict:
        """
        获取md5值，用于判断数据是否改变
        """
        data = {
            "name": self.name,
            "parent_id": self.parent_remote_dept_id,
            "order": self.seq,
        }
        return data
