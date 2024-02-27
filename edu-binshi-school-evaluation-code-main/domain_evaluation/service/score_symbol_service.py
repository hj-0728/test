from typing import List, Optional

from infra_utility.enum_helper import get_enum_value_by_name

from domain_evaluation.model.score_symbol_model import EnumScoreSymbolValueType
from domain_evaluation.repository.score_symbol_repository import ScoreSymbolRepository


class ScoreSymbolService:
    """
    得分符号service
    """

    def __init__(
        self,
        score_symbol_repository: ScoreSymbolRepository,
    ):
        self.__score_symbol_repository = score_symbol_repository

    def get_score_symbol_list(self, value_type_list: List[str]):
        """
        获取得分符号列表
        """
        score_symbol_list = self.__score_symbol_repository.get_score_symbol_list(
            value_type_list=value_type_list
        )
        for score_symbol in score_symbol_list:
            score_symbol.value_type_string = get_enum_value_by_name(
                enum_class=EnumScoreSymbolValueType, enum_name=score_symbol.value_type
            )
        return score_symbol_list
