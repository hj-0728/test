from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from domain_evaluation.entity.score_symbol import ScoreSymbolEntity
from domain_evaluation.model.score_symbol_model import ScoreSymbolModel, ScoreSymbolNameVm


class ScoreSymbolRepository(BasicRepository):
    def insert_score_symbol(self, score_symbol: ScoreSymbolModel, transaction: Transaction):
        """
        插入得分符号
        """
        self._insert_versioned_entity_by_model(
            entity_cls=ScoreSymbolEntity, entity_model=score_symbol, transaction=transaction
        )

    def fetch_score_symbol(self, value_type: Optional[str] = None) -> List[ScoreSymbolModel]:
        """
        获取所有得分符号
        """
        sql = """select * from st_score_symbol"""
        if value_type:
            sql += """ where value_type = :value_type"""
        sql += """ order by value_type, name"""
        return self._fetch_all_to_model(
            model_cls=ScoreSymbolModel, sql=sql, params={"value_type": value_type}
        )

    def get_score_symbol_list(self, value_type_list: List[str]) -> List[ScoreSymbolNameVm]:
        """
        获取所有得分符号
        """
        sql = """
        select value_type, json_agg(row_to_json(s)) as options_list from st_score_symbol s
        """
        if len(value_type_list) > 0:
            sql += """
            where value_type = any(:value_type_list)
            """
        sql += """
        group by value_type
        """
        return self._fetch_all_to_model(
            model_cls=ScoreSymbolNameVm, sql=sql, params={"value_type_list": value_type_list}
        )
