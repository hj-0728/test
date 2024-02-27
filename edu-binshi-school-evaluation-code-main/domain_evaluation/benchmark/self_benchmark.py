from typing import List

from infra_basic.basic_resource import BasicResource

from domain_evaluation.benchmark.basic_benchmark_impl import BasicBenchmarkImpl
from domain_evaluation.data.enum import EnumResource
from domain_evaluation.model.edit.load_filler_em import LoadFillerEditModel


class SelfBenchmark(BasicBenchmarkImpl):
    def load_filler(self, params: LoadFillerEditModel) -> List[BasicResource]:
        """
        加载填充者
        """
        resource = BasicResource(
            category=EnumResource.ESTABLISHMENT_ASSIGN.name, id=params.establishment_assign_id
        )
        return [resource]
