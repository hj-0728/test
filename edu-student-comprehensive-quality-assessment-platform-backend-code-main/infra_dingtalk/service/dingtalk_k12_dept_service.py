from infra_utility.algorithm.tree import list_to_tree

from infra_dingtalk.model.dingtalk_k12_dept_model import EnumDingtalkK12DeptCategory

# from biz_integrated.model.period_category_model import EnumPeriodCategoryCode
# from biz_integrated.repository.period_repository import PeriodRepository
from infra_dingtalk.model.view.dingtalk_k12_dept_vm import DingtalkK12DeptListVm
from infra_dingtalk.repository.dingtalk_k12_dept_repository import DingtalkK12DeptRepository


class DingtalkK12DeptService:
    """
    k12部门 service
    """

    def __init__(
        self,
        dingtalk_k12_dept_repository: DingtalkK12DeptRepository,
        # period_repository: PeriodRepository,
    ):
        self.__dingtalk_k12_dept_repository = dingtalk_k12_dept_repository
        # self.__period_repository = period_repository

    def get_dingtalk_k12_dept_tree_parent_id(
        self,
        parent_id: str = None,
    ):
        """
        获取k12部门列表
        """
        tree_list = self.__dingtalk_k12_dept_repository.get_dingtalk_k12_dept_tree_list_parent_id(
            parent_id=parent_id,
        )
        return list_to_tree(original_list=tree_list, tree_node_type=DingtalkK12DeptListVm)

    # def get_dingtalk_k12_dept_tree(
    #     self, period_id: str, dingtalk_user_id: str, category: str
    # ):
    #     """
    #     获取部门树
    #     """
    #     period_info = self.__period_repository.get_period_by_id(
    #         period_id=period_id
    #     )
    #     semester_period_id = period_id
    #     if period_info:
    #         semester_period_id = period_info.id
    #         if period_info.category_code in [
    #             EnumPeriodCategoryCode.WEEK.name,
    #             EnumPeriodCategoryCode.MONTH.name,
    #         ]:
    #             semester_period_id = period_info.parent_id
    #     tree_list = self.__dingtalk_k12_dept_repository.get_dingtalk_k12_dept_tree(
    #         period_id=semester_period_id,
    #         dingtalk_user_id=dingtalk_user_id,
    #         get_all=True if category == 'get_all' else False,
    #     )
    #     root_dept = self.__dingtalk_k12_dept_repository.get_root_dingtalk_k12_dept()
    #     duty_dingtalk_k12_dept_id_list = self.__dingtalk_k12_dept_repository.get_duty_dingtalk_k12_dept_id_list(
    #         period_id=period_id,
    #         dingtalk_user_id=dingtalk_user_id,
    #     )
    #     for dept in tree_list:
    #         if dept.category == EnumDingtalkK12DeptCategory.SCHOOL_CLASS.name:
    #             if dept.id in duty_dingtalk_k12_dept_id_list:
    #                 dept.can_edit = True
    #             else:
    #                 dept.can_edit = False
    #         if dept.category == EnumDingtalkK12DeptCategory.GRADE.name:
    #             dept.parent_id = root_dept.id
    #     if tree_list:
    #         tree_list.append(DingtalkK12DeptListVm(
    #             id=root_dept.id,
    #             name=root_dept.name,
    #             level=0,
    #             seq=1,
    #             key=root_dept.id,
    #         ))
    #     return list_to_tree(original_list=tree_list, tree_node_type=DingtalkK12DeptListVm)
