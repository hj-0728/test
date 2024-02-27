from typing import List

from infra_basic.basic_resource import BasicResource
from infra_basic.errors import BusinessError

from domain_evaluation.benchmark.basic_benchmark_impl import BasicBenchmarkImpl
from domain_evaluation.data.enum import EnumResource
from domain_evaluation.model.edit.load_filler_em import LoadFillerEditModel


class TeamCategoryBenchmark(BasicBenchmarkImpl):
    def load_filler(self, params: LoadFillerEditModel) -> List[BasicResource]:
        """
        加载填充者
        """
        input_node = self._execute_node_service.load_input_node(
            input_node_id=params.benchmark_input_node_id
        )
        team_category_id = input_node.filler_calc_context.get("team_category_id")
        team_category = self._team_category_repository.fetch_team_category_by_id(
            team_category_id=team_category_id
        )
        if not team_category:
            raise BusinessError(f"未获取到id为【{team_category_id}】的小组类型，请联系技术支持人员。")
        team = self._benchmark_node_assistant_repository.fetch_student_evaluation_team(
            establishment_assign_id=params.establishment_assign_id,
            team_category_id=team_category_id,
        )
        if not team:
            # 因为sql是inner join的，如果没返回数据，就是班级没找到，返回数据了部门一定在
            raise BusinessError(f"未获取到学生id为【{params.establishment_assign_id}】所在的班级，请联系技术支持人员。")
        if not team.filler_id:
            raise BusinessError(f"请为【{team.dept_name}】设置类型为【{team_category.name}】的评价小组。")
        resource = BasicResource(
            category=EnumResource.TEAM.name,
            id=team.filler_id,
        )
        return [resource]
