from typing import List

from infra_basic.basic_resource import BasicResource

from domain_evaluation.benchmark.basic_benchmark_impl import BasicBenchmarkImpl
from domain_evaluation.model.edit.load_filler_em import LoadFillerEditModel


class OtherClassmatesBenchmark(BasicBenchmarkImpl):
    def load_filler(self, params: LoadFillerEditModel) -> List[BasicResource]:
        """
        加载填充者
        因为目前这种类型的评价，先不做，所以这里返回空列表
        等确实有具体业务需要开展了，再用实现相关功能
        """
        return []
