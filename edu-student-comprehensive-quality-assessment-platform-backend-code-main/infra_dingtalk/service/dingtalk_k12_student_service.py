from infra_dingtalk.data.query_params.dingtalk_k12_student_query_params import (
    DingtalkK12StudentQueryParams,
)
from infra_dingtalk.repository.dingtalk_k12_student_repository import DingtalkK12StudentRepository


class DingtalkK12StudentService:
    """
    k12部门 service
    """

    def __init__(self, dingtalk_k12_student_repository: DingtalkK12StudentRepository):
        self._dingtalk_k12_student_repository = dingtalk_k12_student_repository

    def get_dingtalk_k12_student_list_page(
        self,
        query_params: DingtalkK12StudentQueryParams,
        role_code: str,
    ):
        """
        获取k12部门对应的学生
        :param query_params:
        :param role_code:
        :return:
        """
        return self._dingtalk_k12_student_repository.get_dingtalk_k12_student_list_page(
            query_params=query_params, role_code=role_code
        )
