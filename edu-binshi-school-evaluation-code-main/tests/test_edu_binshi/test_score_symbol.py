from domain_evaluation.model.score_symbol_model import EnumScoreSymbolValueType, ScoreSymbolModel
from edu_binshi.data.enum import EnumScoreSymbolCode


def test_score_symbol(prepare_domain_evaluation_container, prepare_robot):
    uow = prepare_domain_evaluation_container.uow()
    symbol_repo = prepare_domain_evaluation_container.score_symbol_repository()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_score_symbol")
        data_list = [
            {
                "name": "星",
                "code": EnumScoreSymbolCode.STAR.name,
                "value_type": EnumScoreSymbolValueType.NUM.name,
                "numeric_precision": 0,
            },
            {
                "name": "等级",
                "code": EnumScoreSymbolCode.GRADE.name,
                "value_type": EnumScoreSymbolValueType.STRING.name,
                "string_options": ["优秀", "良好", "合格", "待评"],
            },
        ]
        for data in data_list:
            symbol_repo.insert_score_symbol(
                score_symbol=ScoreSymbolModel(**data), transaction=trans
            )
