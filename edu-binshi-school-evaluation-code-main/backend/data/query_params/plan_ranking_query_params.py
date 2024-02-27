from typing import Optional, List

from infra_basic.basic_repository import PageFilterParams


class PlanRankingQueryParams(PageFilterParams):
    """
    计划排行
    """

    benchmark_id: str
    evaluation_criteria_plan_id: str
    dimension_dept_tree_id_list: Optional[List[str]]  # 若没有则捞全部
