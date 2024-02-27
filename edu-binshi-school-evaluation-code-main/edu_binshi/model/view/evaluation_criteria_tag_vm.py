from infra_basic.basic_model import BasePlusModel
from typing import Optional


class EvaluationCriteriaTagViewModel(BasePlusModel):
    total_tag_count: int
    root_tag_count: int

    @property
    def tag_level(self) -> Optional[int]:
        if self.total_tag_count:
            # 如果已经打过标签，且根节点的标签大于0，则标签打在第一层，否则打在第二层
            return 1 if self.root_tag_count else 2
        # 如果没打过标签，则返回None，可以告诉前端，由用户自由选择
        return None
