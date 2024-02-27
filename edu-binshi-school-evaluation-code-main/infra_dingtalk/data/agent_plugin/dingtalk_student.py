from typing import List, Optional

from infra_basic.basic_model import BasePlusModel

from infra_dingtalk.data.agent_plugin.dingtalk_parent import DingtalkParent
from infra_dingtalk.model.dingtalk_k12_student_model import DingtalkK12StudentModel


class DingtalkStudent(BasePlusModel):
    """
    学生
    """

    userid: str
    unionid: str
    name: str
    student_no: Optional[str]
    feature: Optional[str]
    class_id: int
    parents: List[DingtalkParent] = []

    department: List[int] = []

    def to_dingtalk_k12_student_em(self, dingtalk_corp_id: str) -> DingtalkK12StudentModel:
        return DingtalkK12StudentModel(
            dingtalk_corp_id=dingtalk_corp_id,
            name=self.name,
            remote_user_id=self.userid,
        )
