from infra_basic.basic_model import BasePlusModel


class ExportReportEditModel(BasePlusModel):
    user_id: str
    role_id: str
    target_category: str
    target_id: str
    evaluation_criteria_plan_id: str
