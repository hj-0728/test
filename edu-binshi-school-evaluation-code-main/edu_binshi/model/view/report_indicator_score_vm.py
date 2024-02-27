from typing import Optional, List, Set

from infra_basic.basic_model import BasePlusModel
from infra_utility.algorithm.tree import TreeNodeModel
from domain_evaluation.model.benchmark_strategy_model import EnumBenchmarkStrategySourceCategory

ORDER = ["自评", "他评", "综合", "等级"]


class ReportBenchmarkViewModel(BasePlusModel):
    name: str
    numeric_score: Optional[float]
    string_score: Optional[str]
    numeric_max_score: Optional[float]
    tag: str
    source_category: Optional[str]

    @property
    def score(self) -> str:
        if self.numeric_score is not None:
            return f"({str(int(self.numeric_score))})★"
        if self.string_score:
            return f"({self.string_score})"
        return ""

    def matched(self, tag: str, name_prefix: str):
        if tag == "综合":
            for i in ["合计", "综合"]:
                if f"{name_prefix}{i}" in self.name:
                    return True
        else:
            if f"{name_prefix}{tag}" in self.name:
                return True


class ReportIndicatorScoreViewModel(TreeNodeModel):
    name: str
    tag: str
    seq: int
    parent_indicator_id: Optional[str]
    indicator_id: str
    level: int
    benchmark_list: List[ReportBenchmarkViewModel]

    def get_child_benchmark_tag(self, tag_set: Set[str]):
        """
        获取子节点的tag
        """
        for child in self.children:
            for benchmark in child.benchmark_list:
                if benchmark.source_category == EnumBenchmarkStrategySourceCategory.INPUT.name:
                    # 这里可能会有一个bug，以【二、行为表现/2.日常课堂表现】为例，这个指标是自评他评的聚合，相应的tag不是自评或他评，而是综合
                    # 在赋分的时候，两个格子的顺序可能会乱，要么就是不判断source_category，这种情况先不显示tag，但是对用户不一定友好
                    tag_set.add(benchmark.tag)
            if child.children:
                child.get_child_benchmark_tag(tag_set=tag_set)
        sorted_items = sorted(tag_set, key=lambda x: ORDER.index(x))
        return sorted_items

    def sort_benchmark_list(self):
        sorted_items = sorted(self.benchmark_list, key=lambda x: ORDER.index(x.tag))
        self.benchmark_list = sorted_items

        score_list = []
        for benchmark in self.benchmark_list:
            if benchmark.numeric_max_score:
                score = f"{str(int(benchmark.numeric_max_score))}★"
                if score not in score_list:
                    score_list.append(score)
        if score_list:
            self.name = f"{self.name}（{'/'.join(score_list)}）"


class RootIndicatorScoreViewModel(BasePlusModel):
    name: str
    benchmark_list: List[ReportBenchmarkViewModel]
