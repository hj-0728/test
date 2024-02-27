from datetime import datetime
from enum import Enum
from typing import Dict, Optional
from infra_utility.datetime_helper import local_now
from pydantic import Field

from infra_basic.basic_model import BasicModel, VersionedModel
from infra_utility.base_plus_model import BasePlusModel


class EnumReportTargetCategory(Enum):
    """
    报告目标类型
    """

    EVALUATION_ASSIGNMENT = "个人"
    DIMENSION_DEPT_TREE = "维度部门"
    ORGANIZATION = "组织"


class EnumReportRecordStatus(Enum):
    """
    报告记录状态
    """

    PENDING = "等待中"
    FAILED = "失败的"
    SUCCEED = "成功的"


class UploadReportModel(BasePlusModel):
    file_bytes: bytes
    file_name: str
    file_relationship_relationship: str
    file_resource_id: Optional[str]
    file_resource_category: Optional[str]


class ReportFileInfoModel(BasicModel):

    url: str
    name: Optional[str]
    relationship: str


class ReportRecordModel(VersionedModel):
    """
    报告记录 model
    """

    created_at: datetime = Field(default_factory=local_now)
    user_role_id: str
    evaluation_criteria_plan_id: str
    target_category: str
    target_id: str
    args: Optional[Dict]
    error: Optional[str]
    status: Optional[str]

    user_id: Optional[str]
    role_id: Optional[str]
