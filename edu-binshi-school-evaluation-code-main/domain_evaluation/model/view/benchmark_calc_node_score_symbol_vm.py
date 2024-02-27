from infra_utility.base_plus_model import BasePlusModel

from domain_evaluation.model.score_symbol_model import ScoreSymbolModel


class BenchmarkCalcNodeScoreSymbolViewModel(BasePlusModel):
    """
    基准计算节点分数符号视图模型
    """

    id: str
    input_score_symbol: ScoreSymbolModel
    output_score_symbol: ScoreSymbolModel
