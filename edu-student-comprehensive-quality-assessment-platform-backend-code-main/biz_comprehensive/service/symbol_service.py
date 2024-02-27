from typing import List, Tuple

from biz_comprehensive.data.constant import PointsConst
from biz_comprehensive.model.symbol_model import EnumSymbolCode
from biz_comprehensive.model.view.symbol_exchange_vm import SymbolExchangeViewModel
from biz_comprehensive.repository.symbol_repository import SymbolRepository


class SymbolService:
    def __init__(self, symbol_repository: SymbolRepository):
        self.__symbol_repository = symbol_repository

    @staticmethod
    def points_exchange_rating_show(
        points: float, symbol_list: List[SymbolExchangeViewModel]
    ) -> Tuple[str, int]:
        """
        积分转换成等级展示
        :param points:
        :param symbol_list:
        :return:
        """
        for symbol in symbol_list:
            value = points // symbol.exchange_rate
            if value > 0:
                if value > PointsConst.MAX_RATING_SHOW_COUNT:
                    return symbol.code, PointsConst.MAX_RATING_SHOW_COUNT
                # 在这个场景下int(value)是可以的，不需要通过精度去转换
                return symbol.code, int(value)
        return EnumSymbolCode.STAR.name, 0
