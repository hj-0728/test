from typing import List

from infra_basic.basic_resource import BasicResource
from infra_basic.errors import BusinessError

from domain_evaluation.benchmark.basic_benchmark_impl import BasicBenchmarkImpl
from domain_evaluation.data.enum import EnumResource
from domain_evaluation.model.edit.load_filler_em import LoadFillerEditModel


class TeacherBenchmark(BasicBenchmarkImpl):
    def load_filler(self, params: LoadFillerEditModel) -> List[BasicResource]:
        """
        加载填充者
        """
        input_node = self._execute_node_service.load_input_node(
            input_node_id=params.benchmark_input_node_id
        )
        subject_id = input_node.filler_calc_context.get("subject_id")
        subject = self._subject_repository.fetch_subject_by_id(subject_id=subject_id)
        if not subject:
            raise BusinessError(f"未获取到id为【{subject_id}】的科目，请联系技术支持人员。")
        teacher = self._benchmark_node_assistant_repository.fetch_student_teacher(
            establishment_assign_id=params.establishment_assign_id, subject_id=subject_id
        )
        if not teacher:
            # 因为sql是inner join的，如果没返回数据，就是班级没找到，返回数据了部门一定在
            raise BusinessError(f"未获取到学生id为【{params.establishment_assign_id}】所在的班级，请联系技术支持人员。")
        if not teacher.filler_id:
            raise BusinessError(f"请为【{teacher.dept_name}】设置【{subject.name}】科目的任课老师。")
        resource = BasicResource(category=EnumResource.ESTABLISHMENT_ASSIGN.name, id=teacher.filler_id)
        return [resource]
