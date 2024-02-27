from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import OrderCondition, PageInitParams
from infra_basic.transaction import Transaction

from domain_evaluation.data.query_params.evaluation_criteria_page_query_params import (
    EvaluationCriteriaPageQueryParams, EvaluationCriteriaListQueryParams,
)
from domain_evaluation.entity.evaluation_criteria import EvaluationCriteriaEntity
from domain_evaluation.model.benchmark_calc_node_model import BenchmarkCalcNodeModel
from domain_evaluation.model.evaluation_criteria_model import EvaluationCriteriaModel
from domain_evaluation.model.evaluation_criteria_plan_model import (
    EnumEvaluationCriteriaPlanStatus,
    EvaluationCriteriaPlanModel,
)
from domain_evaluation.model.view.evaluation_criteria_vm import EvaluationCriteriaVm


class EvaluationCriteriaRepository(BasicRepository):
    """
    评价标准 repository
    """

    def get_evaluation_criteria_by_name(
        self,
        name: str,
        evaluation_object_category: str,
        evaluation_criteria_id: Optional[str],
    ) -> Optional[EvaluationCriteriaModel]:
        """

        通过name和evaluation_object_category获取评价标准
        :param name:
        :param evaluation_object_category:
        :param evaluation_criteria_id:
        :return:
        """
        sql = """
        select * from st_evaluation_criteria 
        where name=:name and evaluation_object_category=:evaluation_object_category 
        """

        if evaluation_criteria_id:
            sql += """
            AND id!=:evaluation_criteria_id
            """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=EvaluationCriteriaModel,
            params={
                "name": name,
                "evaluation_object_category": evaluation_object_category,
                "evaluation_criteria_id": evaluation_criteria_id,
            },
        )

    def insert_evaluation_criteria(
        self,
        evaluation_criteria: EvaluationCriteriaModel,
        transaction: Transaction = None,
    ) -> str:
        """
        插入评价标准
        :param evaluation_criteria:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=EvaluationCriteriaEntity,
            entity_model=evaluation_criteria,
            transaction=transaction,
        )

    def update_evaluation_criteria(
        self,
        evaluation_criteria: EvaluationCriteriaModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新评价标准
        :param evaluation_criteria:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        return self._update_versioned_entity_by_model(
            entity_cls=EvaluationCriteriaEntity,
            update_model=evaluation_criteria,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_evaluation_criteria(
        self,
        evaluation_criteria_id: str,
        transaction: Transaction = None,
    ):
        """
        删除评价标准
        :param evaluation_criteria_id:
        :param transaction:
        :return:
        """
        self._delete_versioned_entity_by_id(
            entity_cls=EvaluationCriteriaEntity,
            entity_id=evaluation_criteria_id,
            transaction=transaction,
        )

    def get_evaluation_criteria_page(
        self,
        params: EvaluationCriteriaPageQueryParams,
    ) -> PaginationCarrier[EvaluationCriteriaModel]:
        """
        :param params:
        :return:
        """

        sql = """
        SELECT id, version, name, status, comments, evaluation_object_category,
        CASE WHEN status = 'DRAFT' THEN 1
        WHEN status = 'PUBLISHED' THEN 2
        ELSE 3
        END AS status_order
        FROM st_evaluation_criteria sc
        WHERE TRUE
        """

        if params.status_list:
            sql += """
            AND sc.status = ANY(:status_list)
            """

        if params.evaluation_object_category_list:
            sql += """
            AND sc.evaluation_object_category = ANY(:evaluation_object_category_list)
            """

        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["name"],
            order_columns=[
                OrderCondition(column_name="status_order", order="asc"),
                OrderCondition(column_name="name", order="asc"),
            ],
            params={
                "status_list": params.status_list,
                "evaluation_object_category_list": params.evaluation_object_category_list,
            },
        )
        return self._paginate(
            result_type=EvaluationCriteriaModel,
            total_params=page_init_params,
            page_params=params,
        )

    def get_evaluation_criteria_detail(
        self,
        evaluation_criteria_id: str,
    ) -> Optional[EvaluationCriteriaVm]:
        """
        获取评价标准详情
        :param evaluation_criteria_id:
        :return:
        """

        sql = """
        SELECT src.id, src.version, src.name, src.status, src.comments, src.evaluation_object_category
        FROM st_evaluation_criteria src
        WHERE src.id = :evaluation_criteria_id
        """

        return self._fetch_first_to_model(
            model_cls=EvaluationCriteriaVm,
            sql=sql,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
            },
        )

    def fetch_benchmark_calc_node_by_evaluation_criteria_id(
        self,
        evaluation_criteria_id: str,
    ) -> List[BenchmarkCalcNodeModel]:
        """
        获取评价标准的计算节点
        :param evaluation_criteria_id:
        :return:
        """

        sql = """
        select cn.* 
        from st_evaluation_criteria c 
        INNER JOIN st_evaluation_criteria_tree t on c.id=t.evaluation_criteria_id
        INNER JOIN st_indicator i on i.id=t.indicator_id
        INNER JOIN st_benchmark b on b.indicator_id=i.id 
        INNER JOIN st_benchmark_execute_node en on en.benchmark_id=b.id
        INNER JOIN st_benchmark_calc_node cn on cn.benchmark_execute_node_id=en.id
        WHERE c.id = :evaluation_criteria_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=BenchmarkCalcNodeModel,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
            },
        )

    def get_evaluation_criteria_plan_by_evaluation_criteria_id(
        self,
        evaluation_criteria_id: str,
    ) -> List[EvaluationCriteriaPlanModel]:
        """
        获取应用评价标准的评价标准计划
        :param evaluation_criteria_id:
        :return:
        """
        sql = """
        SELECT * FROM st_evaluation_criteria_plan cp 
        WHERE cp.evaluation_criteria_id = :evaluation_criteria_id
        AND cp.status != :status
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=EvaluationCriteriaPlanModel,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
                "status": EnumEvaluationCriteriaPlanStatus.ABOLISHED.name,
            },
        )

    def get_evaluation_criteria_list(
        self,
        params: EvaluationCriteriaListQueryParams,
    ) -> List[EvaluationCriteriaModel]:
        """
        :param params:
        :return:
        """

        sql = """
        SELECT id, version, name, status, comments, evaluation_object_category
        FROM st_evaluation_criteria sc
        WHERE TRUE
        """

        if params.status_list:
            sql += """
            AND sc.status = ANY(:status_list)
            """

        if params.evaluation_object_category_list:
            sql += """
            AND sc.evaluation_object_category = ANY(:evaluation_object_category_list)
            """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=EvaluationCriteriaModel,
            params={
                "status_list": params.status_list,
                "evaluation_object_category_list": params.evaluation_object_category_list,
            },
        )

    def get_evaluation_criteria_by_id(
        self,
        evaluation_criteria_id: str,
    ) -> Optional[EvaluationCriteriaModel]:
        """
        获取应用评价标准的评价标准计划
        :param evaluation_criteria_id:
        :return:
        """
        sql = """
        SELECT * FROM st_evaluation_criteria WHERE id = :evaluation_criteria_id
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=EvaluationCriteriaModel,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
            },
        )
