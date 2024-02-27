from typing import Optional

from infra_basic.basic_model import BasePlusModel


class BenchmarkFillerViewModel(BasePlusModel):
    filler_id: Optional[str]
    dept_name: str
