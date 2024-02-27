from infra_basic.basic_repository import BasicRepository

from domain_evaluation.model.evaluation_criteria_plan_model import EnumEvaluationCriteriaPlanStatus
from domain_evaluation.model.input_score_log_model import EnumExpectedFillerCategory


class AppEvaluationCriteriaPlanRepository(BasicRepository):
    def fetch_team_execute_plan_count(self, team_id: str) -> int:
        """
        获取小组正在执行的计划数
        """
        sql = """
        select sp.* from st_evaluation_criteria_plan sp
        inner join st_evaluation_assignment sa on sp.id = sa.evaluation_criteria_plan_id
        inner join st_input_score_log sl on sl.evaluation_assignment_id = sa.id
        and sl.expected_filler_category = :team_category and expected_filler_id = :team_id
        where sp.status = :status and executed_start_at <= now() and now() <= executed_finish_at
        """
        return self._fetch_count(
            sql=sql,
            params={
                "team_id": team_id,
                "team_category": EnumExpectedFillerCategory.TEAM.name,
                "status": EnumEvaluationCriteriaPlanStatus.PUBLISHED.name
            },
        )
