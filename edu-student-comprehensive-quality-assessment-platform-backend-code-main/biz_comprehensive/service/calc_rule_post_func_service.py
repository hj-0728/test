from biz_comprehensive.model.calc_rule_model import CalcRuleModel
from biz_comprehensive.model.edit.calc_em import CalcResourceEditModel
from biz_comprehensive.model.view.calc_result_vm import FuncCalcResultLogViewModel


class CalcRulePostFuncService:
    """
    计算规则后置方法
    """

    def execute_calc_rule_post_func(
        self,
        calc_rule: CalcRuleModel,
        resource_data: CalcResourceEditModel,
    ) -> FuncCalcResultLogViewModel:
        """
        执行计算规则后置方法
        :param calc_rule:
        :param resource_data:
        :return:
        """

        if not calc_rule.post_func:
            return FuncCalcResultLogViewModel(
                func=None,
                func_args=None,
            )

        pre_func = getattr(self, calc_rule.post_func)

        calc_result = pre_func(
            calc_rule=calc_rule,
            resource_data=resource_data,
            args=calc_rule.post_func_params,
        )

        post_func_params = calc_rule.post_func_params if calc_rule.post_func_params else {}

        return FuncCalcResultLogViewModel(
            func=calc_rule.calc_func,
            func_args=post_func_params
            | {"calc_rule": calc_rule.dict()}
            | {"resource_data": resource_data.dict()},
            calc_result=calc_result,
        )
