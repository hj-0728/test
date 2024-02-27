from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from domain_evaluation.entity.benchmark_score import BenchmarkScoreEntity
from domain_evaluation.model.benchmark_score_model import BenchmarkScoreModel
from domain_evaluation.model.view.benchmark_node_score_tree_vm import BenchmarkNodeScoreTreeModel


class BenchmarkScoreRepository(BasicRepository):
    """
    度量单元分数 repository
    """

    def insert_benchmark_score(
        self,
        benchmark_score: BenchmarkScoreModel,
        transaction: Transaction,
    ) -> str:
        """
        插入基准分数
        :param benchmark_score:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=BenchmarkScoreEntity, entity_model=benchmark_score, transaction=transaction
        )

    def update_benchmark_score(
        self,
        benchmark_score: BenchmarkScoreModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        修改基准分数
        :param benchmark_score:
        :param transaction:
        :param limited_col_list:
        :return:
        """

        return self._update_versioned_entity_by_model(
            entity_cls=BenchmarkScoreEntity,
            update_model=benchmark_score,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def fetch_calc_benchmark_score_need_node_info(
        self, benchmark_id: str, evaluation_assignment_id: str
    ) -> List[BenchmarkNodeScoreTreeModel]:
        """
        获取计算基准分数需要的节点信息
        :param benchmark_id:
        :param evaluation_assignment_id:
        :return:
        """

        sql = """
        WITH current_node as (
        select en.*,ino.id as detail_node from st_benchmark_execute_node en
        INNER JOIN st_benchmark_input_node ino on en.id=ino.benchmark_execute_node_id
        where en.benchmark_id=:benchmark_id 
        and now()>ino.start_at and now()<=ino.finish_at
        UNION
        select en.*,cn.id as detail_node from st_benchmark_execute_node en
        INNER JOIN st_benchmark_calc_node cn on en.id=cn.benchmark_execute_node_id
        where en.benchmark_id=:benchmark_id
        )
        , input_value as (
        select n.id,sl.numeric_score,sl.string_score,sl.id as source_score_id,
        'INPUT_LOG' as source_score_category
        from current_node n 
        INNER JOIN sv_current_input_score_log sl on sl.benchmark_input_node_id=n.detail_node
        where evaluation_assignment_id=:evaluation_assignment_id
        union
        select n.id ,bs.numeric_score,bs.string_score, 
        bs.id as source_score_id,'BENCHMARK_SCORE' as source_score_category
        from current_node n 
        INNER JOIN st_benchmark_input_node ino on n.detail_node=ino.id
        INNER JOIN st_benchmark_score bs on ino.source_benchmark_id=bs.benchmark_id
        and bs.evaluation_assignment_id=:evaluation_assignment_id
        )
        , calc_info as (
        select nt.id,sl.id as calc_score_log_id 
        from current_node nt
        INNER JOIN sv_current_calc_score_log sl on sl.benchmark_calc_node_id=nt.detail_node
        where sl.evaluation_assignment_id=:evaluation_assignment_id
        )
        select nt.*, iv.numeric_score,iv.string_score,source_score_id,
        source_score_category,calc_score_log_id
        from current_node nt 
        LEFT JOIN input_value iv on nt.id=iv.id
        LEFT JOIN calc_info ci on ci.id=nt.id
        ORDER BY seq
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=BenchmarkNodeScoreTreeModel,
            params={
                "benchmark_id": benchmark_id,
                "evaluation_assignment_id": evaluation_assignment_id,
            },
        )

    def fetch_benchmark_score_by_evaluation_assignment_id_and_benchmark_id(
        self, evaluation_assignment_id: str, benchmark_id: str
    ) -> Optional[BenchmarkScoreModel]:
        """
        获取基准分数
        :param evaluation_assignment_id:
        :param benchmark_id:
        :return:
        """

        sql = """
        select * from st_benchmark_score 
        where evaluation_assignment_id=:evaluation_assignment_id 
        and benchmark_id=:benchmark_id
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=BenchmarkScoreModel,
            params={
                "evaluation_assignment_id": evaluation_assignment_id,
                "benchmark_id": benchmark_id,
            }
        )
