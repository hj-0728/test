"""
k12学生信息
"""

from typing import List

from infra_basic.basic_model import BasePlusModel

from infra_dingtalk.model.dingtalk_k12_family_relationship_model import (
    DingtalkK12FamilyRelationshipModel,
)
from infra_dingtalk.model.dingtalk_k12_parent_model import DingtalkK12ParentModel
from infra_dingtalk.model.view.dingtalk_k12_dept_student_vm import DingtalkK12DeptStudentViewModel


class DingtalkK12StudentDetailViewModel(BasePlusModel):
    """
    k12学生信息
    """

    id: str
    version: int
    name: str
    dingtalk_corp_id: str
    remote_user_id: str
    remote_dept_ids: List[int]
    dept_list: List[DingtalkK12DeptStudentViewModel]
    parent_list: List[DingtalkK12ParentModel] = []
    relationship_list: List[DingtalkK12FamilyRelationshipModel] = []
