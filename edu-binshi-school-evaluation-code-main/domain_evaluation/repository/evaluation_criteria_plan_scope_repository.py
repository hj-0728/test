from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from domain_evaluation.entity.evaluation_criteria_plan_scope import (
    EvaluationCriteriaPlanScopeEntity,
)
from domain_evaluation.model.evaluation_criteria_plan_model import \
    EnumEvaluationCriteriaPlanStatus
from domain_evaluation.model.evaluation_criteria_plan_scope_model import (
    EnumGroupCategory,
    EvaluationCriteriaPlanScopeCategoryModal,
    EvaluationCriteriaPlanScopeModel,
)
from infra_backbone.model.dimension_model import EnumDimensionCategory


class EvaluationCriteriaPlanScopeRepository(BasicRepository):
    """
    评价标准计划适用的集合 repository
    """

    def insert_evaluation_criteria_plan_scope(
        self,
        data: EvaluationCriteriaPlanScopeModel,
        transaction: Transaction = None,
    ) -> str:
        """
        插入评价标准计划适用的集合
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=EvaluationCriteriaPlanScopeEntity,
            entity_model=data,
            transaction=transaction,
        )

    def update_evaluation_criteria_plan_scope(
        self,
        data: EvaluationCriteriaPlanScopeModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新评价标准计划适用的集合
        :param data:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        return self._update_versioned_entity_by_model(
            entity_cls=EvaluationCriteriaPlanScopeEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_evaluation_criteria_plan_scope(
        self, delete_evaluation_criteria_plan_scope_id: str, transaction: Transaction
    ):
        """
        删除评价标准计划适用的集合
        :param delete_evaluation_criteria_plan_scope_id:
        :param transaction:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=EvaluationCriteriaPlanScopeEntity,
            entity_id=delete_evaluation_criteria_plan_scope_id,
            transaction=transaction,
        )

    def get_plan_scope_by_plan_id_and_scope(
        self,
        evaluation_criteria_plan_id: str,
        scope_category: str,
        scope_id_list: List[str] = None
    ) -> List[EvaluationCriteriaPlanScopeModel]:
        """
        根据plan_id和scope_id获取评价标准集合适用集合
        :param evaluation_criteria_plan_id:
        :param scope_category:
        :param scope_id_list:
        :return:
        """

        sql = """
        with scope as (
        SELECT *, rank() OVER (PARTITION BY scope_id ORDER BY ps.handled_at DESC) AS seq
        FROM st_evaluation_criteria_plan_scope ps 
        WHERE ps.evaluation_criteria_plan_id = :evaluation_criteria_plan_id 
        and finish_at>now() and scope_category=:scope_category
        """

        if scope_id_list:
            sql += " AND ps.scope_id = any(array[:scope_id_list]) "
        sql += ") select * from scope where seq=1 "

        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaPlanScopeModel,
            sql=sql,
            params={
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
                "scope_category": scope_category,
                "scope_id_list": scope_id_list,
            },
        )

    def get_plan_scope_by_plan_id(
        self,
        plan_id: str,
    ) -> List[EvaluationCriteriaPlanScopeCategoryModal]:
        """
        根据plan_id获取评价标准计划适用的集合
        :param plan_id:
        :return:
        """
        sql = """
        WITH people_info AS ( 
            SELECT ea.id AS establishment_assign_id, sp.* 
            FROM st_establishment_assign ea 
            INNER JOIN st_people_history sp ON sp.id = ea.people_id 
        ) 
        SELECT
        cp.id AS evaluation_criteria_plan_id,
        ps.scope_category,
        CASE
            WHEN ps.scope_category = :PERSONAL THEN
                JSONB_AGG ( JSONB_BUILD_OBJECT ( 'id', ps.scope_id, 'name', pi.NAME,
                'is_deleted', not pi.is_available)) 
            WHEN ps.scope_category = :DEPT THEN
            JSONB_AGG ( JSONB_BUILD_OBJECT ( 'id', ps.scope_id, 'name',
            case when sd3.name is null then sd.NAME else sd3.name || '/' || sd.NAME end,
            'is_deleted', case when sd.finish_at>now() then false else true end)
            ORDER BY sd3.name,sd.NAME) 
            WHEN ps.scope_category IS NULL THEN NULL
            ELSE
                TO_JSONB ( ARRAY_AGG ( ps.scope_id ) )
        END AS scope_info
        FROM
            ( select *,LEAST(handled_at, executed_finish_at) as least_time from st_evaluation_criteria_plan) cp
            LEFT JOIN st_evaluation_criteria_plan_scope ps 
            ON ps.evaluation_criteria_plan_id = cp.id AND ps.finish_at > now()
            LEFT JOIN st_dept_history sd ON ps.scope_id = sd.ID and (
            ((cp.status=:ABOLISHED or (cp.status!=:DRAFT and cp.executed_finish_at<now())
            ) and (least_time BETWEEN sd.begin_at and sd.end_at)) or 
            ((cp.status=:DRAFT or (cp.status!=:ABOLISHED and cp.executed_finish_at>now())
            ) and sd.end_at>now()))
            left join st_dimension_dept_tree_history sddt on sddt.dept_id = sd.id and (
            ((cp.status=:ABOLISHED or (cp.status!=:DRAFT and cp.executed_finish_at<now())
            ) and (least_time BETWEEN sddt.begin_at and sddt.end_at)) or 
            ((cp.status=:DRAFT or (cp.status!=:ABOLISHED and cp.executed_finish_at>now())
            ) and sddt.end_at>now()))
            left join st_dimension sd2 on sd2.id = sddt.dimension_id and sd2.category =:EDU
            left join st_dept_history sd3 on sd3.id = sddt.parent_dept_id and (
            ((cp.status=:ABOLISHED or (cp.status!=:DRAFT and cp.executed_finish_at<now())
            ) and (least_time BETWEEN sd3.begin_at and sd3.end_at)) or 
            ((cp.status=:DRAFT or (cp.status!=:ABOLISHED and cp.executed_finish_at>now())
            ) and sd3.end_at>now()))
            AND ps.scope_category = :DEPT
            LEFT JOIN people_info pi ON ps.scope_id = pi.establishment_assign_id and (
            ((cp.status=:ABOLISHED or (cp.status!=:DRAFT and cp.executed_finish_at<now())
            ) and (least_time BETWEEN pi.begin_at and pi.end_at)) or 
            ((cp.status=:DRAFT or (cp.status!=:ABOLISHED and cp.executed_finish_at>now())
            ) and pi.end_at>now()))
            AND ps.scope_category = :PERSONAL
        WHERE
            cp.id = :plan_id
        GROUP BY
            cp.id, ps.scope_category, cp.executed_finish_at
        """
        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaPlanScopeCategoryModal,
            sql=sql,
            params={
                "plan_id": plan_id,
                "PERSONAL": EnumGroupCategory.PERSONAL.name,
                "DEPT": EnumGroupCategory.DEPT.name,
                "EDU": EnumDimensionCategory.EDU.name,
                "ABOLISHED": EnumEvaluationCriteriaPlanStatus.ABOLISHED.name,
                "DRAFT": EnumEvaluationCriteriaPlanStatus.DRAFT.name,
            },
        )

    def get_evaluation_criteria_plan_scope_list_by_plan_id(
        self, evaluation_criteria_plan_id: str, scope_category: Optional[str]
    ) -> List[EvaluationCriteriaPlanScopeModel]:
        """
        根据plan_id获取评价计划适用集合
        :param evaluation_criteria_plan_id:
        :param scope_category:
        :return:
        """
        sql = """
        SELECT * FROM st_evaluation_criteria_plan_scope ps 
        WHERE ps.evaluation_criteria_plan_id = :evaluation_criteria_plan_id
        AND ps.finish_at > now()
        """
        if scope_category:
            sql += """
            AND ps.scope_category = :scope_category
            """
        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaPlanScopeModel,
            sql=sql,
            params={
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
                "scope_category": scope_category,
            },
        )
