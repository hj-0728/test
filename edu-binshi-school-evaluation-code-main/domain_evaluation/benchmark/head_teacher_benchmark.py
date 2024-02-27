from typing import List

from infra_basic.basic_resource import BasicResource
from infra_basic.errors import BusinessError

from domain_evaluation.benchmark.basic_benchmark_impl import BasicBenchmarkImpl
from domain_evaluation.data.enum import EnumResource
from domain_evaluation.model.edit.load_filler_em import LoadFillerEditModel


class HeadTeacherBenchmark(BasicBenchmarkImpl):
    def load_filler(self, params: LoadFillerEditModel) -> List[BasicResource]:
        """
        加载填充者
        """
        teacher = self._benchmark_node_assistant_repository.fetch_student_head_teacher(
            establishment_assign_id=params.establishment_assign_id
        )
        if not teacher:
            # 因为sql是inner join的，如果没返回数据，就是班级没找到，返回数据了部门一定在
            raise BusinessError(f"未获取到学生id为【{params.establishment_assign_id}】所在的班级，请联系技术支持人员。")
        if not teacher.filler_id:
            raise BusinessError(f"请为【{teacher.dept_name}】设置班主任。")
        resource = BasicResource(category=EnumResource.ESTABLISHMENT_ASSIGN.name, id=teacher.filler_id)
        return [resource]
