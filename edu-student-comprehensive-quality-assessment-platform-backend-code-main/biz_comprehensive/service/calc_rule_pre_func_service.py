from typing import Any, List, Optional

from biz_comprehensive.model.calc_rule_model import CalcRuleModel
from biz_comprehensive.model.edit.calc_em import CalcResourceEditModel
from biz_comprehensive.model.view.calc_result_vm import (
    CalcResultViewModel,
    FuncCalcResultLogViewModel,
)
from biz_comprehensive.repository.calc_rule_pre_depends_repository import (
    CalcRulePreDependsRepository,
)
from infra_backbone.data.enum import EnumBackboneResource
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.repository.establishment_assign_repository import EstablishmentAssignRepository


class CalcRulePreFuncService:
    """
    计算规则前置方法
    """

    def __init__(
        self,
        calc_rule_pre_depends_repository: CalcRulePreDependsRepository,
        establishment_assign_repository: EstablishmentAssignRepository,
    ):
        self.__calc_rule_pre_depends_repository = calc_rule_pre_depends_repository
        self.__establishment_assign_repository = establishment_assign_repository

    def execute_calc_rule_pre_func(
        self,
        calc_rule: CalcRuleModel,
        resource_data: CalcResourceEditModel,
    ) -> FuncCalcResultLogViewModel:
        """
        执行计算规则前置方法
        :param calc_rule:
        :param resource_data:
        :return:
        """

        if not calc_rule.pre_func:
            return FuncCalcResultLogViewModel(
                func=None,
                func_args=None,
            )

        pre_func = getattr(self, calc_rule.pre_func)

        calc_result = pre_func(
            calc_rule=calc_rule,
            resource_data=resource_data,
            args=calc_rule.pre_func_params,
        )

        pre_func_params = calc_rule.pre_func_params if calc_rule.pre_func_params else {}

        return FuncCalcResultLogViewModel(
            func=calc_rule.pre_func,
            func_args=pre_func_params
            | {"calc_rule": calc_rule.dict()}
            | {"resource_data": resource_data.dict()},
            calc_result=calc_result,
        )

    def get_indicator_pre_depends_score(
        self,
        calc_rule: CalcRuleModel,
        resource_data: CalcResourceEditModel,
        args: Optional[Any],
    ) -> List[CalcResultViewModel]:
        """
        获取指标前置依赖分数
        :param calc_rule:
        :param resource_data:
        :param args:
        :return:
        """

        pass

    def get_res_symbol_score(
        self,
        calc_rule: CalcRuleModel,
        resource_data: CalcResourceEditModel,
        args: Optional[Any],
    ) -> List[CalcResultViewModel]:
        """
        获取需要计算的对象
        :param calc_rule:
        :param resource_data:
        :param args:
        :return:
        """

        pass

    def handle_calc_object(
        self,
        calc_rule: CalcRuleModel,
        resource_data: CalcResourceEditModel,
        args: Optional[Any],
    ) -> List[CalcResultViewModel]:
        """
        处理需要计算的对象
        :param calc_rule:
        :param resource_data:
        :param args:
        :return:
        """

        pre_result_list = [resource_data.cast_to(CalcResultViewModel)]

        if resource_data.owner_res_category == EnumBackboneResource.DIMENSION_DEPT_TREE.name:
            res_list = self.__establishment_assign_repository.get_establishment_assign_by_dept_tree_id_and_capacity_code(
                dimension_dept_tree_id=resource_data.owner_res_id,
                capacity_code=EnumCapacityCode.STUDENT.name,
            )
            for res in res_list:
                pre_result_list.append(
                    CalcResultViewModel(
                        owner_res_category=EnumBackboneResource.ESTABLISHMENT_ASSIGN.name,
                        owner_res_id=res.id,
                    )
                )

        return pre_result_list
