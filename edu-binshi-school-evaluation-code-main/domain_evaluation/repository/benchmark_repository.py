from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from domain_evaluation.entity.benchmark import BenchmarkEntity
from domain_evaluation.model.benchmark_model import BenchmarkModel, BenchmarkVm
from domain_evaluation.model.benchmark_strategy.basic_schema import NameValuePair
from domain_evaluation.model.benchmark_strategy.grade_schema import GradeItem
from domain_evaluation.model.score_symbol_model import EnumScoreSymbolValueType
from domain_evaluation.model.view.benchmark_score_symbol_model import \
    BenchmarkScoreSymbolViewModel
from domain_evaluation.model.view.sub_level_indicator_tree_vm import \
    SubLevelIndicatorTreeItem


class BenchmarkRepository(BasicRepository):
    """
    度量单元 repository
    """

    def insert_benchmark(
        self,
        benchmark: BenchmarkModel,
        transaction: Transaction,
    ) -> str:
        """
        插入基准
        :param benchmark:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=BenchmarkEntity, entity_model=benchmark, transaction=transaction
        )

    def update_benchmark(
        self,
        benchmark: BenchmarkModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新基准
        :param benchmark:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        return self._update_versioned_entity_by_model(
            entity_cls=BenchmarkEntity,
            update_model=benchmark,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_benchmark(
        self,
        benchmark_id: str,
        transaction: Transaction = None,
    ):
        """
        删除基准
        :param benchmark_id:
        :param transaction:
        :return:
        """
        self._delete_versioned_entity_by_id(
            entity_cls=BenchmarkEntity, entity_id=benchmark_id, transaction=transaction
        )

    def fetch_benchmark_by_id(self, benchmark_id: str) -> BenchmarkModel:
        """
        通过 id 获取基准
        :param benchmark_id:
        :return:
        """
        sql = """
        select * from st_benchmark where id=:benchmark_id
        """
        return self._fetch_first_to_model(
            model_cls=BenchmarkModel, sql=sql, params={"benchmark_id": benchmark_id}
        )

    def fetch_current_benchmark_as_other_source(self, benchmark_id: str) -> int:
        """
        获取当前基准作为其他benchmark的输入源的个数
        """
        sql = """
        select sb.* from st_benchmark_input_node sin
        inner join st_benchmark_execute_node sen on sin.benchmark_execute_node_id = sen.id
        inner join st_benchmark sb on sb.id = sen.benchmark_id
        and sb.start_at < now() and now() < sb.finish_at
        where sin.source_benchmark_id = :benchmark_id
        """
        return self._fetch_count(sql=sql, params={"benchmark_id": benchmark_id})

    def get_benchmark_list_by_indicator_id(self, indicator_id: str, input_score_symbol_id: str):
        """
        获取指标的所有基准(相同symbol的)
        """
        sql = """
        select sb.* from st_benchmark sb 
        inner join st_benchmark_execute_node be on be.benchmark_id = sb.id
        inner join st_benchmark_input_node bi on bi.benchmark_execute_node_id = be.id
        inner join st_score_symbol ss on ss.id = bi.score_symbol_id
        where sb.indicator_id = :indicator_id
        and sb.finish_at > now() and ss.id = :input_score_symbol_id
        """
        return self._fetch_all_to_model(
            sql=sql,
            params={
                "indicator_id": indicator_id,
                "input_score_symbol_id": input_score_symbol_id,
            },
            model_cls=BenchmarkVm,
        )

    def fetch_indicator_same_symbol_benchmark(
        self, indicator_id: str, score_symbol_id, benchmark_id: Optional[str]
    ) -> List[NameValuePair]:
        """
        加载同一指标的下符号类型相同的基准
        用来做权重计算的选项
        """
        sql = """select name, id as value, null as weight from cv_benchmark sb
        where sb.indicator_id = :indicator_id
        and benchmark_strategy_params ->> 'scoreSymbolId' = :score_symbol_id
        """
        if benchmark_id:
            sql += """
            and sb.id != :benchmark_id
            """
        sql += """
        order by sb.name
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=NameValuePair,
            params={"indicator_id": indicator_id, "score_symbol_id": score_symbol_id, "benchmark_id": benchmark_id},
        )

    def fetch_sub_indicator_same_symbol_benchmark(
        self, indicator_id: str, score_symbol_id
    ) -> List[SubLevelIndicatorTreeItem]:
        """
        加载同一指标的下符号类型相同的基准
        用来做权重计算的选项
        """
        sql = """ 
        WITH RECURSIVE evaluation_criteria_tree AS (
        select si.name, si.id as value, null::text as parent_id,
        ct.seq,ARRAY[si.id::text] AS parent_id_list
        from cv_evaluation_criteria_tree ct 
        INNER JOIN st_indicator si on si.id = ct.indicator_id 
        where ct.parent_indicator_id =:indicator_id and si.is_activated is true
        UNION
        select si.name, si.id as value, ct.parent_indicator_id as parent_id,ct.seq,
        array_append(ec.parent_id_list, si.id::text) AS parent_id_list
        from cv_evaluation_criteria_tree ct 
        INNER JOIN st_indicator si on si.id = ct.indicator_id and si.is_activated is true
        INNER JOIN evaluation_criteria_tree ec on ec.value = ct.parent_indicator_id 
        )
        , benchmark as (
        select cb.name,cb.id as value, ct.indicator_id as parent_id,ct.seq,
        true as checkable,ec.parent_id_list
        from cv_benchmark cb
        INNER JOIN st_indicator si on si.id = cb.indicator_id  and si.is_activated is true
        INNER JOIN cv_evaluation_criteria_tree ct on ct.indicator_id = si.id
        INNER JOIN evaluation_criteria_tree ec on ec.value = ct.indicator_id
        and benchmark_strategy_params ->> 'scoreSymbolId' =:score_symbol_id
        )
        , info as (
        select * from benchmark
        UNION
        select t.name,t.value,t.parent_id,t.seq,false as checkable,t.parent_id_list
        from evaluation_criteria_tree t 
        INNER JOIN benchmark b on t.value=any(b.parent_id_list)
        )
        select name,value,parent_id,checkable,
        rank() over(ORDER BY checkable desc,parent_id,seq) as seq
        from info 
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=SubLevelIndicatorTreeItem,
            params={"indicator_id": indicator_id, "score_symbol_id": score_symbol_id},
        )

    def fetch_same_level_num_benchmark(self, indicator_id: str) -> List[GradeItem]:
        """
        加载同一指标的下数值类型符号的基准
        作为区间取值的入参
        """
        sql = """
        select sb.name, json_build_object('source_benchmark_id', sb.id, 'input_score_symbol_id', sy.id) as value
        from cv_benchmark sb
        inner join st_score_symbol sy on sy.id = benchmark_strategy_params ->> 'scoreSymbolId'
        and sy.value_type = :value_type
        where sb.indicator_id = :indicator_id
        order by sb.name
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=GradeItem,
            params={"indicator_id": indicator_id, "value_type": EnumScoreSymbolValueType.NUM.name},
        )

    def fetch_specific_version_benchmark(
        self, benchmark_id: str, benchmark_version: int
    ) -> BenchmarkModel:
        """
        通过id和版本号获取基准
        :param benchmark_id:
        :param benchmark_version:
        :return:
        """
        sql = """
        select * from st_benchmark where id=:benchmark_id and version=:benchmark_version
        """
        return self._fetch_first_to_model(
            model_cls=BenchmarkModel,
            sql=sql,
            params={"benchmark_id": benchmark_id, "benchmark_version": benchmark_version},
        )

    def get_benchmark_detail_by_id(self, benchmark_id: str) -> Optional[BenchmarkVm]:
        """
        通过id获取基准
        """
        sql = """
        select cb.*,ti.id as tag_id from cv_benchmark cb 
        inner join sv_tag_info ti on ti.resource_id = cb.id
        where cb.id=:benchmark_id 
        """
        return self._fetch_first_to_model(
            model_cls=BenchmarkVm,
            sql=sql,
            params={"benchmark_id": benchmark_id}
        )

    def fetch_benchmark_list(self, indicator_id: str) -> List[BenchmarkModel]:
        """
        获取同一指标下的所有未删除的基准
        """
        sql = """
        select * from cv_benchmark where indicator_id = :indicator_id
        """
        return self._fetch_all_to_model(
            model_cls=BenchmarkModel,
            sql=sql,
            params={
                "indicator_id": indicator_id
            }
        )

    def fetch_current_benchmark_as_parent_source(self, indicator_id: str) -> int:
        """
        获取当前基准作为父级benchmark的输入源的个数
        """
        sql = """
        with recursive evaluation_criteria_tree as (
        select si.id, si.name
        from cv_evaluation_criteria_tree ct
        INNER JOIN st_indicator si on si.id = ct.indicator_id
        where ct.indicator_id = :indicator_id
        UNION
        select  si.id, si.name
        from cv_evaluation_criteria_tree ct
        INNER JOIN st_indicator si on si.id = ct.indicator_id
        INNER JOIN evaluation_criteria_tree ec on ec.id = ct.parent_indicator_id
        ),
        benchmark as (
        select sb.*
        from cv_benchmark sb
        INNER JOIN evaluation_criteria_tree ct on ct.id= sb.indicator_id
        )
        select sin.* from cv_benchmark_input_node sin
        inner join st_benchmark_execute_node sen on sin.benchmark_execute_node_id = sen.id
        where sin.source_benchmark_id in (select id from benchmark)
        and sen.benchmark_id not in (select id from benchmark)
        """
        return self._fetch_count(sql=sql, params={"indicator_id": indicator_id})

    def get_benchmark_score_symbol(
        self, benchmark_id: str
    ) -> Optional[BenchmarkScoreSymbolViewModel]:
        """
        获取基准的得分符号
        :param benchmark_id:
        :return:
        """

        sql = """
        select sy.*,b.benchmark_strategy_params ->> 'limitedStringOptions' as limited_string_options_str,
        b.benchmark_strategy_params ->> 'numericMaxScore' as numeric_max_score,
        b.benchmark_strategy_params ->> 'numericMinScore' as numeric_min_score
        from st_benchmark b
        inner join st_score_symbol sy 
        on sy.id = b.benchmark_strategy_params ->> 'scoreSymbolId'
        where b.id=:benchmark_id
        """

        return self._fetch_first_to_model(
            model_cls=BenchmarkScoreSymbolViewModel,
            sql=sql,
            params={"benchmark_id": benchmark_id}
        )

    def fetch_benchmark_by_input_node_id(self, input_node_id: str) -> Optional[BenchmarkModel]:
        """
        通过input_node_id获取基准
        """
        sql = """
        select sb.* from st_benchmark sb
        inner join st_benchmark_execute_node sen on sen.benchmark_id = sb.id
        inner join st_benchmark_input_node sin on sin.benchmark_execute_node_id = sen.id
        where sin.id = :input_node_id
        """
        return self._fetch_first_to_model(
            model_cls=BenchmarkModel,
            sql=sql,
            params={"input_node_id": input_node_id}
        )

    def fetch_benchmark_reference_list(self, source_benchmark_id: str):
        """
        获取基准的引用列表
        """
        sql = """
        select distinct sb.* from cv_benchmark sb
        join st_benchmark_execute_node sen on sen.benchmark_id = sb.id
        join st_benchmark_input_node sin on sin.benchmark_execute_node_id = sen.id
        where sin.source_benchmark_id = :source_benchmark_id and sin.finish_at > now()
        """
        return self._fetch_all_to_model(
            model_cls=BenchmarkModel,
            sql=sql,
            params={"source_benchmark_id": source_benchmark_id}
        )
