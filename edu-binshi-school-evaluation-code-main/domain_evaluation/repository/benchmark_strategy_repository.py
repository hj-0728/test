from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from domain_evaluation.entity.benchmark_strategy import BenchmarkStrategyEntity
from domain_evaluation.model.benchmark_strategy_model import BenchmarkStrategyModel
from domain_evaluation.model.view.benchmark_strategy_vm import BenchmarkStrategyInfoVm


class BenchmarkStrategyRepository(BasicRepository):
    def insert_benchmark_strategy(
        self, benchmark_strategy: BenchmarkStrategyModel, transaction: Transaction
    ):
        """
        插入基准策略
        :param benchmark_strategy:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=BenchmarkStrategyEntity,
            entity_model=benchmark_strategy,
            transaction=transaction,
        )

    def fetch_benchmark_strategy_list(self) -> List[BenchmarkStrategyModel]:
        """
        获取基准策略
        :return:
        """
        sql = """select * from cv_benchmark_strategy order by name"""
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=BenchmarkStrategyModel,
        )

    def fetch_benchmark_strategy_by_id(self, strategy_id: str) -> Optional[BenchmarkStrategyModel]:
        """
        获取基准策略
        """
        sql = """select * from cv_benchmark_strategy where id = :strategy_id"""
        return self._fetch_first_to_model(
            sql=sql, model_cls=BenchmarkStrategyModel, params={"strategy_id": strategy_id}
        )

    def fetch_benchmark_strategy_by_code(self, code: str) -> Optional[BenchmarkStrategyModel]:
        """
        获取基准策略
        """
        sql = """select * from cv_benchmark_strategy where code = :code"""
        return self._fetch_first_to_model(
            sql=sql, model_cls=BenchmarkStrategyModel, params={"code": code}
        )

    def get_benchmark_strategy_list(self) -> List[BenchmarkStrategyInfoVm]:
        """
        获取基准策略
        :return:
        """
        sql = """
        select bs.*,tor.tag_ownership_id from cv_benchmark_strategy bs 
        inner join st_tag_ownership_relationship tor on tor.resource_id = bs.id
        order by name
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=BenchmarkStrategyInfoVm,
        )
