from abc import ABC, abstractmethod
from typing import List

from infra_basic.basic_resource import BasicResource

from domain_evaluation.model.edit.load_filler_em import LoadFillerEditModel


class BasicBenchmark(ABC):
    @abstractmethod
    def load_filler(self, params: LoadFillerEditModel) -> List[BasicResource]:
        pass
