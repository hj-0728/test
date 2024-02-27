from typing import Optional

from infra_utility.base_plus_model import BasePlusModel


class DimensionDeptTreeReportInfoVm(BasePlusModel):
    """
    维度部门树报告信息 vm
    """

    evaluation_criteria_plan_name: str
    evaluation_criteria_name: str
    dept_name: str
    period_name: str
    dimension_dept_tree_id: Optional[str]


class ExistEstablishmentAssignReportVm(BasePlusModel):
    """
    个人报告 vm
    """

    file_id: str
    object_name: str
    bucket_name: str
    file_relationship_relationship: str


class OrganizationReportInfoVm(BasePlusModel):
    """
    组织报告信息 vm
    """

    evaluation_criteria_plan_name: str
    evaluation_criteria_name: str
    organization_name: str
    period_name: str


class EvaluationAssignmentReportFileVM(BasePlusModel):
    """
    报告文件
    """

    doc_file_bytes: bytes
    pdf_file_bytes: bytes

