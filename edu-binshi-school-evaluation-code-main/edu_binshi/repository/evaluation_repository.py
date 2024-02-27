from typing import Optional

from infra_basic.basic_repository import BasicRepository

from domain_evaluation.model.evaluation_assignment_model import \
    EnumEvaluationAssignmentEffectedCategory
from edu_binshi.model.view.evaluation_assignment_vm import EvaluationAssignmentViewModel
from edu_binshi.model.view.evaluation_criteria_plan_vm import EvaluationCriteriaPlanVM


class EvaluationRepository(BasicRepository):
    """
    评价 repository
    """

    def fetch_evaluation_criteria_plan_by_id(
        self, evaluation_criteria_plan_id: str
    ) -> Optional[EvaluationCriteriaPlanVM]:
        """
        通过 id 获取评价标准计划
        :param evaluation_criteria_plan_id:
        :return:
        """

        sql = """
        select cp.*,p.name as period_name
        from st_evaluation_criteria_plan cp 
        inner join st_period p on cp.focus_period_id=p.id
        where cp.id = :evaluation_criteria_plan_id
        """

        return self._fetch_first_to_model(
            model_cls=EvaluationCriteriaPlanVM,
            params={
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
            },
            sql=sql,
        )

    def fetch_evaluation_assignment_info(
        self, evaluation_assignment_id: str
    ) -> Optional[EvaluationAssignmentViewModel]:
        """
        获取计划信息及分配的学生姓名
        :param evaluation_assignment_id:
        :return:
        """

        sql = """
        select ea.*,cp.name as plan_name,p.name as period_name,sp.name as people_name
        from st_evaluation_assignment ea 
        INNER JOIN st_evaluation_criteria_plan cp on ea.evaluation_criteria_plan_id=cp.id
        inner join st_period p on cp.focus_period_id=p.id
        inner join st_establishment_assign sa on sa.id=ea.effected_id 
        and ea.effected_category = :effected_category
        inner join st_people sp on sp.id =sa.people_id
        where ea.id=:evaluation_assignment_id
        """

        return self._fetch_first_to_model(
            model_cls=EvaluationAssignmentViewModel,
            params={
                "evaluation_assignment_id": evaluation_assignment_id,
                "effected_category": EnumEvaluationAssignmentEffectedCategory.ESTABLISHMENT_ASSIGN.name,
            },
            sql=sql,
        )
