from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.symbol import SymbolEntity
from biz_comprehensive.entity.symbol_exchange import SymbolExchangeEntity
from biz_comprehensive.model.symbol_exchange_model import SymbolExchangeModel
from biz_comprehensive.model.symbol_model import EnumSymbolCategory, EnumSymbolCode, SymbolModel
from biz_comprehensive.model.view.symbol_exchange_vm import SymbolExchangeViewModel


class SymbolRepository(BasicRepository):
    def insert_symbol(self, data: SymbolModel, transaction: Transaction):
        """
        插入符号
        """
        self._insert_versioned_entity_by_model(
            entity_cls=SymbolEntity, entity_model=data, transaction=transaction
        )

    def insert_symbol_exchange(self, data: SymbolExchangeModel, transaction: Transaction):
        """
        插入符号兑换
        """
        self._insert_versioned_entity_by_model(
            entity_cls=SymbolExchangeEntity, entity_model=data, transaction=transaction
        )

    def fetch_symbol_by_code(self, code: str) -> Optional[SymbolModel]:
        """
        获取符号根据code
        :return:
        """

        sql = """
        select * from st_symbol where code=:code
        """

        return self._fetch_first_to_model(model_cls=SymbolModel, sql=sql, params={"code": code})

    def fetch_rating_show_symbol_exchange(self) -> List[SymbolExchangeViewModel]:
        """
        获取符号兑换列表
        :return:
        """

        sql = """
        select sy.name, sy.code, se.exchange_rate
        from st_symbol sy
        inner join st_symbol_exchange se on se.source_symbol_id = sy.id
        inner join st_symbol sy2 on sy2.id = se.target_symbol_id and sy2.code = :points
        where sy.category = :rating_show
        order by se.exchange_rate desc
        """
        return self._fetch_all_to_model(
            model_cls=SymbolExchangeViewModel,
            sql=sql,
            params={
                "points": EnumSymbolCode.POINTS.name,
                "rating_show": EnumSymbolCategory.RATING_SHOW.name,
            },
        )
