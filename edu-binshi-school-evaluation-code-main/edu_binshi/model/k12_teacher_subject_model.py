"""
k12教师科目模型类
"""

from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel
from infra_utility.datetime_helper import local_now


class K12TeacherSubjectModel(VersionedModel):
    """
    k12教师科目
    """

    people_id: str
    dimension_dept_tree_id: str
    subject_id: str
    start_at: datetime = local_now()
    finish_at: Optional[datetime]
