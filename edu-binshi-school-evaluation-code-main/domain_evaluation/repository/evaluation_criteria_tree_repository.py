from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from domain_evaluation.data.enum import (
    EnumResource,
    EnumTagOwnerCategory,
    EnumTagOwnershipRelationship,
)
from domain_evaluation.data.query_params.evaluation_criteria_tree_item_query_params import (
    EvaluationCriteriaBoundTagItemQueryParams,
    EvaluationCriteriaNotBoundTagItemQueryParams,
)
from domain_evaluation.entity.evaluation_criteria_tree import EvaluationCriteriaTreeEntity
from domain_evaluation.model.benchmark_input_node_model import BenchmarkInputNodeSourceCategory
from domain_evaluation.model.evaluation_criteria_tree_model import (
    EvaluationCriteriaTreeInfoModel,
    EvaluationCriteriaTreeModel,
)
from domain_evaluation.model.evaluation_criteria_tree_node_model import (
    EvaluationCriteriaTreeNodeModel,
)
from domain_evaluation.model.view.evaluation_criteria_tree_item_vm import (
    EvaluationCriteriaTreeItemViewModel,
)
from domain_evaluation.model.view.evaluation_criteria_tree_vm import EvaluationCriteriaTreeViewModel
from edu_binshi.model.view.evaluation_criteria_tag_vm import EvaluationCriteriaTagViewModel


class EvaluationCriteriaTreeRepository(BasicRepository):
    """
    评价标准的树（对用户可以叫评价项） repository
    """

    def insert_evaluation_criteria_tree(
        self,
        evaluation_criteria_tree: EvaluationCriteriaTreeModel,
        transaction: Transaction = None,
    ) -> str:
        """
        插入评价标准的树（对用户可以叫评价项）
        :param evaluation_criteria_tree:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=EvaluationCriteriaTreeEntity,
            entity_model=evaluation_criteria_tree,
            transaction=transaction,
        )

    def update_evaluation_criteria_tree(
        self,
        evaluation_criteria_tree: EvaluationCriteriaTreeModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新评价标准的树（对用户可以叫评价项）
        :param evaluation_criteria_tree:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        return self._update_versioned_entity_by_model(
            entity_cls=EvaluationCriteriaTreeEntity,
            update_model=evaluation_criteria_tree,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_evaluation_criteria_tree(
        self,
        evaluation_criteria_tree_id: str,
        transaction: Transaction = None,
    ):
        """
        删除评价标准的树（对用户可以叫评价项）
        :param evaluation_criteria_tree_id:
        :param transaction:
        :return:
        """
        self._delete_versioned_entity_by_id(
            entity_cls=EvaluationCriteriaTreeEntity,
            entity_id=evaluation_criteria_tree_id,
            transaction=transaction,
        )

    def get_exist_evaluation_criteria_tree(
        self,
        evaluation_criteria_id: str,
        parent_id: str = None,
    ):
        """
        获取已经存在的评价标准的树（对用户可以叫评价项）
        :param evaluation_criteria_id:
        :param parent_id:
        :return:
        """

        sql = """
        SELECT * FROM st_evaluation_criteria_tree
        WHERE evaluation_criteria_id = :evaluation_criteria_id
        """

        if parent_id:
            sql += """
            AND parent_id = :parent_id
            """
        else:
            sql += """
            AND parent_id IS NULL
            """

        return self._fetch_first_to_model(
            model_cls=EvaluationCriteriaTreeModel,
            sql=sql,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
                "parent_id": parent_id,
            },
        )

    def get_evaluation_criteria_tree(
        self, evaluation_criteria_id: str
    ) -> List[EvaluationCriteriaTreeNodeModel]:
        """
        获取评价标准树
        :return:
        """

        sql = """
        WITH RECURSIVE evaluation_criteria_tree AS (
        SELECT sect.id, sect.id AS key, sect.version,sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        ARRAY[sect.seq] AS seq_list,1 AS level,ARRAY[sect.id::character varying] AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        WHERE sect.parent_indicator_id IS NULL AND sect.evaluation_criteria_id = :evaluation_criteria_id
        and si.is_activated IS True
        UNION ALL
        SELECT sect.id, sect.id AS key, sect.version, sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        array_append(t.seq_list, sect.seq) AS seq_list,t.level + 1 AS level,
        array_append(t.path_list, sect.id) AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        INNER JOIN evaluation_criteria_tree t ON t.indicator_id = sect.parent_indicator_id
        and si.is_activated IS True
        ),
        benchmark_list as(
        select si.indicator_id,sb.id as benchmark_id,sb.name,sb.guidance,
        sb.version as benchmark_version,bs.id as benchmark_strategy_id,bs.code as benchmark_strategy_code,bs.source_category
        from evaluation_criteria_tree si 
        INNER JOIN cv_benchmark sb on sb.indicator_id = si.indicator_id 
        inner join st_benchmark_strategy bs on bs.id = sb.benchmark_strategy_id
        order by sb.name
        ),
        group_benchmark_list as (
        select indicator_id,json_agg(json_build_object(
        'id',bl.benchmark_id,'name',bl.name,'guidance',bl.guidance,'version',bl.benchmark_version,
        'benchmark_strategy_id',bl.benchmark_strategy_id,'benchmark_strategy_code',bl.benchmark_strategy_code,'source_category',bl.source_category
        )) as benchmark_list
        from benchmark_list bl
         GROUP BY indicator_id
        )
        SELECT e.*,si.name as tag,benchmark_list
        FROM evaluation_criteria_tree e
        left join sv_tag_info si on si.resource_id = e.id and si.resource_category = :evaluation_criteria_tree
        and si.relationship = :relationship
        left join group_benchmark_list bl on bl.indicator_id = e.indicator_id
        ORDER BY seq_list
        """

        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaTreeNodeModel,
            sql=sql,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
                "evaluation_criteria_tree": EnumResource.EVALUATION_CRITERIA_TREE.name,
                "relationship": EnumTagOwnershipRelationship.EVALUATION.name,
            },
        )

    def get_evaluation_criteria_tree_max_seq(
        self,
        evaluation_criteria_id: str,
        parent_indicator_id: str = None,
    ):
        """
        获取已经存在的评价标准的树（对用户可以叫评价项）
        :param evaluation_criteria_id:
        :param parent_indicator_id:
        :return:
        """

        sql = """
        SELECT COALESCE(MAX(seq), 0) AS seq FROM cv_evaluation_criteria_tree
        WHERE evaluation_criteria_id = :evaluation_criteria_id
        """

        if parent_indicator_id:
            sql += """
            AND parent_indicator_id = :parent_indicator_id
            """
        else:
            sql += """
            AND parent_indicator_id IS NULL
            """

        data = self._execute_sql(
            sql=sql,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
                "parent_indicator_id": parent_indicator_id,
            },
        )
        if data:
            return data[0].get("seq", 0)
        else:
            return 0

    def get_evaluation_criteria_tree_children(
        self,
        indicator_id: str = None,
    ) -> List[EvaluationCriteriaTreeNodeModel]:
        """
        获取部门树
        :param indicator_id:
        :return:
        """

        sql = """
        WITH RECURSIVE evaluation_criteria_tree AS (
        SELECT sect.id, sect.id AS key, sect.version,'root'::text as parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        ARRAY[sect.seq] AS seq_list,1 AS level,ARRAY[sect.indicator_id::character varying] AS path_list, sect.seq,si.name
        FROM st_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        """

        if indicator_id:
            sql += """
            AND sect.indicator_id = :indicator_id
            """
        else:
            sql += """
            AND sect.parent_indicator_id IS NULL
            """

        sql += """
        where sect.finish_at > now()
        UNION ALL
        SELECT sect.id, sect.id AS key, sect.version, sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        array_append(t.seq_list, sect.seq) AS seq_list,t.level + 1 AS level,
        array_append(t.path_list, sect.indicator_id) AS path_list, sect.seq,si.name
        FROM st_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        INNER JOIN evaluation_criteria_tree t ON t.indicator_id = sect.parent_indicator_id
        where sect.finish_at > now()
        )
        SELECT *
        FROM evaluation_criteria_tree
        WHERE is_activated IS True
        """

        if indicator_id:
            sql += """
            AND :indicator_id = ANY(path_list)
            """

        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaTreeNodeModel,
            sql=sql,
            params={
                "indicator_id": indicator_id,
            },
        )

    def fetch_evaluation_criteria_tree_detail(
        self,
        evaluation_criteria_tree_id: str,
    ) -> Optional[EvaluationCriteriaTreeInfoModel]:
        """
        获取评价标准的树（对用户可以叫评价项）
        :param evaluation_criteria_tree_id:
        :return:
        """

        sql = """
        select t.* ,si.version as indicator_version, si.name, si.comments ,st.tag_ownership_id
        from cv_evaluation_criteria_tree t
        inner join st_indicator si on si.id = t.indicator_id
        left join st_tag_ownership_relationship st on st.resource_id = t.id
        where t.id = :evaluation_criteria_tree_id
        """

        return self._fetch_first_to_model(
            model_cls=EvaluationCriteriaTreeInfoModel,
            sql=sql,
            params={
                "evaluation_criteria_tree_id": evaluation_criteria_tree_id,
            },
        )

    def get_evaluation_criteria_tree_by_evaluation_criteria_id(
        self,
        evaluation_criteria_id: str,
    ) -> List[EvaluationCriteriaTreeModel]:
        """
        获取评价标准的树（对用户可以叫评价项）
        :param evaluation_criteria_id:
        :return:
        """

        sql = """
        SELECT st.*
        FROM st_evaluation_criteria_tree st
        WHERE st.evaluation_criteria_id = :evaluation_criteria_id
        """

        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaTreeModel,
            sql=sql,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
            },
        )

    def get_evaluation_criteria_tree_with_all_benchmark(
        self,
        evaluation_criteria_id: str,
        evaluation_criteria_plan_id: str,
        evaluation_assignment_id: str,
    ) -> List[EvaluationCriteriaTreeViewModel]:
        """
        获取评价标准树跟对应的所有基准
        :param evaluation_criteria_id:
        :param evaluation_criteria_plan_id:
        :param evaluation_assignment_id:
        :return:
        """

        sql = """
        WITH RECURSIVE evaluation_criteria_tree as (
        SELECT id, name, comments, evaluation_criteria_tree_id,
        evaluation_criteria_id, seq, parent_indicator_id, tag_code,
        ARRAY[id::text] AS parent_id_list, 1 AS level,
        ARRAY[seq] AS sort_info, evaluation_criteria_name
        FROM sv_evaluation_criteria_plan_indicator
        WHERE parent_indicator_id is null and evaluation_criteria_id = :evaluation_criteria_id
        and plan_id = :evaluation_criteria_plan_id
        UNION
        SELECT pi.id, pi.name, pi.comments, pi.evaluation_criteria_tree_id,
        pi.evaluation_criteria_id, pi.seq, pi.parent_indicator_id, pi.tag_code,
        array_append(ect.parent_id_list, pi.id) AS parent_dept_id_list,
        ect.level + 1 AS level, array_append(ect.sort_info, pi.seq) AS sort_info,
        ect.evaluation_criteria_name
        FROM sv_evaluation_criteria_plan_indicator pi
        JOIN evaluation_criteria_tree ect ON ect.id = pi.parent_indicator_id
        where plan_id = :evaluation_criteria_plan_id
        ), benchmark_info as (
        SELECT DISTINCT indicator_id, benchmark_id, benchmark_name, score_symbol_name, 
        score_symbol_code, evaluation_criteria_name, evaluation_criteria_id, compare_at,
        benchmark_source_category,
        CASE
        WHEN (bin.limited_string_options IS NOT NULL) THEN isl.string_score
        WHEN (bin.numeric_max_score IS NOT NULL OR bin.numeric_min_score IS NOT NULL) 
        THEN cast(round(isl.numeric_score, bin.score_symbol_numeric_precision) as VARCHAR)
        END AS score_result
        FROM mv_benchmark_input_node bin
        LEFT JOIN st_input_score_log isl on bin.id = isl.benchmark_input_node_id
        and isl.evaluation_assignment_id = :evaluation_assignment_id
        WHERE source_category = 'INPUT' and plan_id = :evaluation_criteria_plan_id
        UNION ALL
        SELECT DISTINCT indicator_id, bcn.benchmark_id, benchmark_name, 
        ss.name as score_symbol_name, ss.code as score_symbol_code, 
        evaluation_criteria_name, evaluation_criteria_id, compare_at,
        benchmark_source_category,
        CASE
        WHEN (bs.string_score IS NOT NULL) THEN bs.string_score
        WHEN (bs.numeric_score IS NOT NULL) 
        THEN cast(round(bs.numeric_score, ss.numeric_precision) as VARCHAR)
        END AS score_result
        FROM mv_benchmark_clac_node bcn 
        LEFT JOIN st_benchmark_score bs on bcn.benchmark_id = bs.benchmark_id
        and bs.evaluation_assignment_id = :evaluation_assignment_id
        LEFT JOIN st_score_symbol ss on bcn.output_score_symbol_id = ss.id
        WHERE plan_id = :evaluation_criteria_plan_id
        ), benchmark_simple_list as (
        SELECT indicator_id, json_agg(json_build_object('benchmark_id', benchmark_id, 
        'benchmark_name', benchmark_name, 'score_symbol_name', score_symbol_name, 
        'score_symbol_code', score_symbol_code, 'score_result', score_result,
        'benchmark_source_category', benchmark_source_category) 
        ORDER BY benchmark_name) as benchmark_simple_list
        FROM benchmark_info
        GROUP BY indicator_id
        ) SELECT ect.id, ect.name, ect.comments, ect.evaluation_criteria_tree_id, ect.tag_code,
        ect.evaluation_criteria_id, ect.evaluation_criteria_name, ect.parent_indicator_id,
        ect.parent_id_list, ect.seq, ect.level, ect.sort_info, bsl.benchmark_simple_list
        FROM evaluation_criteria_tree ect 
        LEFT JOIN benchmark_simple_list bsl on ect.id = bsl.indicator_id
        order by ect.sort_info
        """

        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaTreeViewModel,
            sql=sql,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
                "source_category": BenchmarkInputNodeSourceCategory.INPUT.name,
                "evaluation_assignment_id": evaluation_assignment_id,
            },
        )

    def get_evaluation_criteria_tree_by_indicator_id(
        self,
        indicator_id: str,
    ) -> EvaluationCriteriaTreeInfoModel:
        """
        根据indicator_id获取评价标准树及其tag
        :param indicator_id:
        :return:
        """

        sql = """
        select ct.*,tor.tag_ownership_id  from st_evaluation_criteria_tree ct
        inner join st_tag_ownership_relationship tor ON tor.resource_id = ct.id and tor.resource_category = :resource_category
        where indicator_id=:indicator_id
        """

        return self._fetch_first_to_model(
            model_cls=EvaluationCriteriaTreeInfoModel,
            sql=sql,
            params={
                "indicator_id": indicator_id,
                "resource_category": EnumTagOwnerCategory.EVALUATION_CRITERIA_TREE.name,
            },
        )

    def get_all_child_tree_by_indicator_id(self, indicator_id: str):
        """
        根据指标找到当前指标及其所有子节点
        """

        sql = """
         WITH RECURSIVE evaluation_criteria_tree AS (
         SELECT si.id,
            si.name,
            si.comments,
            ct.id AS evaluation_criteria_tree_id,
            ct.evaluation_criteria_id,
            ct.seq,
            ct.parent_indicator_id,
            ARRAY[si.id::text] AS parent_id_list,
            1 AS level,
            ARRAY[ct.seq] AS sort_info
           FROM st_indicator si
             JOIN st_evaluation_criteria_tree ct ON si.id::text = ct.indicator_id::text
          WHERE si.is_activated IS TRUE AND now() >= ct.start_at AND now() <= ct.finish_at AND ct.parent_indicator_id IS NULL
        UNION
         SELECT si.id,
            si.name,
            si.comments,
            ct.id AS evaluation_criteria_tree_id,
            ct.evaluation_criteria_id,
            ct.seq,
            ct.parent_indicator_id,
            array_append(ect_1.parent_id_list, ct.id::text) AS parent_dept_id_list,
            ect_1.level + 1 AS level,
            array_append(ect_1.sort_info, ct.seq) AS sort_info
           FROM st_indicator si
             JOIN st_evaluation_criteria_tree ct ON si.id::text = ct.indicator_id::text
             JOIN evaluation_criteria_tree ect_1 ON ect_1.id::text = ct.parent_indicator_id::text
          WHERE si.is_activated IS TRUE AND now() >= ct.start_at AND now() <= ct.finish_at
        )
       SELECT t.* ,tor.id as tag_ownership_relationship_id FROM evaluation_criteria_tree t 
        INNER JOIN st_tag_ownership_relationship tor on tor.resource_id = t.evaluation_criteria_tree_id
        where :indicator_id = any(t.parent_id_list)
        """
        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaTreeInfoModel,
            sql=sql,
            params={"indicator_id": indicator_id},
        )

    def get_all_child_tree_by_tree_id_list(self, evaluation_criteria_tree_id_list: List[str]):
        """
        根据指标树id找到当前指标及其所有子节点
        """

        sql = """
         WITH RECURSIVE evaluation_criteria_tree AS (
        SELECT sect.id, sect.id AS key, sect.version,sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        ARRAY[sect.seq] AS seq_list,1 AS level,ARRAY[sect.id::character varying] AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        WHERE si.is_activated IS True and sect.id = ANY(:evaluation_criteria_tree_id_list)
        UNION ALL
        SELECT sect.id, sect.id AS key, sect.version, sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        array_append(t.seq_list, sect.seq) AS seq_list,t.level + 1 AS level,
        array_append(t.path_list, sect.id) AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        INNER JOIN evaluation_criteria_tree t ON t.indicator_id = sect.parent_indicator_id
        and si.is_activated IS True
        )
         SELECT e.*
        FROM evaluation_criteria_tree e
        """
        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaTreeInfoModel,
            sql=sql,
            params={"evaluation_criteria_tree_id_list": evaluation_criteria_tree_id_list},
        )

    def get_evaluation_criteria_tree_bound_tag_item_list(
        self, query_params: EvaluationCriteriaBoundTagItemQueryParams
    ):
        """
        获取绑定标签的评价项列表
        """
        sql = """
        WITH RECURSIVE evaluation_criteria_tree AS (
        SELECT sect.id, sect.id AS key, sect.version,sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        ARRAY[sect.seq] AS seq_list,1 AS level,ARRAY[sect.id::character varying] AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        WHERE sect.evaluation_criteria_id = :evaluation_criteria_id  and parent_indicator_id is null
        and si.is_activated IS True
        UNION ALL
        SELECT sect.id, sect.id AS key, sect.version, sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        array_append(t.seq_list, sect.seq) AS seq_list,t.level + 1 AS level,
        array_append(t.path_list, sect.id) AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        INNER JOIN evaluation_criteria_tree t ON t.indicator_id = sect.parent_indicator_id
        and si.is_activated IS True
        ),
        result as (
         SELECT e.*, case when si.tag_ownership_relationship_id is null then false else true end as is_selected,
         si.name as tag_name, si.tag_ownership_relationship_id
        FROM evaluation_criteria_tree e
        left join sv_tag_info si on si.resource_id = e.id and si.resource_category = :evaluation_criteria_tree
        and si.relationship = :relationship
         )
         select *
        from result where (tag_name = :tag_name or tag_ownership_relationship_id is null) and level = :level
        and is_selected = :is_selected
        """
        return self._fetch_all_to_model(
            sql=sql,
            params={
                "evaluation_criteria_id": query_params.evaluation_criteria_id,
                "evaluation_criteria_tree": EnumResource.EVALUATION_CRITERIA_TREE.name,
                "relationship": EnumTagOwnershipRelationship.EVALUATION.name,
                "tag_name": query_params.tag_name,
                "level": query_params.level,
                "is_selected": query_params.is_selected,
            },
            model_cls=EvaluationCriteriaTreeItemViewModel,
        )

    def get_evaluation_criteria_tree_bound_tag_detail(self, evaluation_criteria_id: str):
        """
        获取评价标准绑定标签情况
        """
        sql = """
        select count(st.*) as total_tag_count,
        count(st.*) filter (where st.parent_indicator_id is null) as root_tag_count
        from st_evaluation_criteria_tree st
        inner join sv_tag_info si on si.resource_id = st.id and si.resource_category = :evaluation_criteria_tree
        and si.relationship = :relationship
        where st.evaluation_criteria_id = :evaluation_criteria_id
        """
        return self._fetch_first_to_model(
            model_cls=EvaluationCriteriaTagViewModel,
            sql=sql,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
                "evaluation_criteria_tree": EnumResource.EVALUATION_CRITERIA_TREE.name,
                "relationship": EnumTagOwnershipRelationship.EVALUATION.name,
            },
        )

    def get_evaluation_criteria_tree_not_bound_tag_item_list(
        self, query_params: EvaluationCriteriaNotBoundTagItemQueryParams
    ):
        """
        获取绑定标签的评价项列表
        """
        sql = """
        WITH RECURSIVE evaluation_criteria_tree AS (
        SELECT sect.id, sect.id AS key, sect.version,sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        ARRAY[sect.seq] AS seq_list,1 AS level,ARRAY[sect.id::character varying] AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        WHERE sect.parent_indicator_id IS NULL AND sect.evaluation_criteria_id = :evaluation_criteria_id
        and si.is_activated IS True
        UNION ALL
        SELECT sect.id, sect.id AS key, sect.version, sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        array_append(t.seq_list, sect.seq) AS seq_list,t.level + 1 AS level,
        array_append(t.path_list, sect.id) AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        INNER JOIN evaluation_criteria_tree t ON t.indicator_id = sect.parent_indicator_id
        and si.is_activated IS True
        )
         SELECT e.*
        FROM evaluation_criteria_tree e
        where not exists(select 1 from sv_tag_info si
        where si.resource_id = e.id and si.resource_category = :evaluation_criteria_tree
        and si.relationship = :relationship
        ) and e.level = :level
        """
        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaTreeItemViewModel,
            sql=sql,
            params={
                "evaluation_criteria_id": query_params.evaluation_criteria_id,
                "evaluation_criteria_tree": EnumResource.EVALUATION_CRITERIA_TREE.name,
                "relationship": EnumTagOwnershipRelationship.EVALUATION.name,
                "level": query_params.level,
            },
        )

    def get_evaluation_criteria_tree_list_by_parent_tree_id_list(
        self, parent_tree_id_list: List[str]
    ):
        """
        根据父节点id列表获取评价标准树列表
        """
        sql = """
        WITH RECURSIVE evaluation_criteria_tree AS (
        SELECT sect.id, sect.id AS key, sect.version,sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        ARRAY[sect.seq] AS seq_list,1 AS level,ARRAY[sect.id::character varying] AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        WHERE sect.parent_indicator_id IS NULL AND sect.evaluation_criteria_id = :evaluation_criteria_id
        and si.is_activated IS True and sect.id = ANY(:parent_tree_id_list)
        UNION ALL
        SELECT sect.id, sect.id AS key, sect.version, sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        array_append(t.seq_list, sect.seq) AS seq_list,t.level + 1 AS level,
        array_append(t.path_list, sect.id) AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        INNER JOIN evaluation_criteria_tree t ON t.indicator_id = sect.parent_indicator_id
        and si.is_activated IS True
        )
         SELECT e.*
        FROM evaluation_criteria_tree e
        """
        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaTreeItemViewModel,
            sql=sql,
            params={
                "parent_tree_id_list": parent_tree_id_list,
            },
        )

    def get_all_child_tree_by_evaluation_criteria_tree_id(self, evaluation_criteria_tree_id: str):
        """
        根据指标树id找到当前指标及其所有子节点
        """

        sql = """
         WITH RECURSIVE evaluation_criteria_tree AS (
        SELECT sect.id, sect.id AS key, sect.version,sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        ARRAY[sect.seq] AS seq_list,1 AS level,ARRAY[sect.id::character varying] AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        WHERE sect.parent_indicator_id IS NULL
        and si.is_activated IS True and sect.id = :evaluation_criteria_tree_id
        UNION ALL
        SELECT sect.id, sect.id AS key, sect.version, sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        array_append(t.seq_list, sect.seq) AS seq_list,t.level + 1 AS level,
        array_append(t.path_list, sect.id) AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        INNER JOIN evaluation_criteria_tree t ON t.indicator_id = sect.parent_indicator_id
        and si.is_activated IS True
        )
         SELECT e.*, si.tag_ownership_relationship_id
        FROM evaluation_criteria_tree e
         join sv_tag_info si on si.resource_id = e.id and si.resource_category = :evaluation_criteria_tree
        and si.relationship = :relationship
        """
        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaTreeItemViewModel,
            sql=sql,
            params={
                "evaluation_criteria_tree_id": evaluation_criteria_tree_id,
                "evaluation_criteria_tree": EnumResource.EVALUATION_CRITERIA_TREE.name,
                "relationship": EnumTagOwnershipRelationship.EVALUATION.name,
            },
        )

    def get_evaluation_criteria_tree_by_evaluation_criteria_id_and_tag_name(
        self, evaluation_criteria_tree_id_list: List[str], tag_name: str
    ):
        """
        根据评价标准id和标签名获取评价标准树
        """
        sql = """
        WITH RECURSIVE evaluation_criteria_tree AS (
        SELECT sect.id, sect.id AS key, sect.version,sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        ARRAY[sect.seq] AS seq_list,1 AS level,ARRAY[sect.id::character varying] AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        WHERE sect.id = ANY(:evaluation_criteria_tree_id_list)
        and si.is_activated IS True
        UNION ALL
        SELECT sect.id, sect.id AS key, sect.version, sect.parent_indicator_id, sect.indicator_id,
        sect.evaluation_criteria_id,
        si.comments,si.is_activated, si.version as indicator_version,
        array_append(t.seq_list, sect.seq) AS seq_list,t.level + 1 AS level,
        array_append(t.path_list, sect.id) AS path_list, sect.seq,si.name,
        sect.start_at,sect.finish_at
        FROM cv_evaluation_criteria_tree sect
        INNER JOIN st_indicator si on si.id = sect.indicator_id
        INNER JOIN evaluation_criteria_tree t ON t.indicator_id = sect.parent_indicator_id
        and si.is_activated IS True
        )
        SELECT e.*,si.tag_ownership_relationship_id
        FROM evaluation_criteria_tree e
        left join sv_tag_info si on si.resource_id = e.id and si.resource_category = :evaluation_criteria_tree
        and si.relationship = :relationship
        where si.name = :tag_name
        """
        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaTreeItemViewModel,
            sql=sql,
            params={
                "evaluation_criteria_tree_id_list": evaluation_criteria_tree_id_list,
                "evaluation_criteria_tree": EnumResource.EVALUATION_CRITERIA_TREE.name,
                "relationship": EnumTagOwnershipRelationship.EVALUATION.name,
                "tag_name": tag_name,
            },
        )
