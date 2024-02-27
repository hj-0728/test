from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumBenchmarkExecuteNodeCategory(str, Enum):
    """
    基准执行节点类型
    """

    INPUT = "输入类型"
    CALC = "计算类型"


class BenchmarkExecuteNodeModel(VersionedModel):
    benchmark_id: str
    name: str
    category: str
    next_node_id: Optional[str]
    seq: int = 1
