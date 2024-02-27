"""
command
"""
from infra_basic.basic_model import BasePlusModel


class SaveBenchmarkScoreEm(BasePlusModel):
    """
    保存基准得分
    """

    benchmark_id: str
    evaluation_assignment_id: str

    @property
    def value(self) -> str:
        return f"{self.benchmark_id}&&{self.evaluation_assignment_id}"
