from typing import Dict, Optional

from domain_evaluation.model.benchmark_strategy.basic_schema import BasicSchema


class ScoreSymbolSchema(BasicSchema):
    item_params: Optional[Dict[str, BasicSchema]]
