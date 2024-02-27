from decimal import Decimal
from typing import Any, List, Optional

from infra_basic.errors import BusinessError

from biz_comprehensive.model.calc_rule_model import CalcRuleModel
from biz_comprehensive.model.view.calc_result_vm import (
    CalcResultViewModel,
    FuncCalcResultLogViewModel,
)


class CalcRuleCalcFuncService:
    """
    计算规则计算方法
    """

    def execute_calc_rule_calc_func(
        self,
        calc_rule: CalcRuleModel,
        pre_result: List[CalcResultViewModel],
    ) -> FuncCalcResultLogViewModel:
        """
        执行计算规则计算方法
        :param calc_rule:
        :param pre_result:
        :return:
        """

        calc_func = getattr(self, calc_rule.calc_func.lower())

        calc_result = calc_func(
            pre_result=pre_result,
            args=calc_rule.calc_func_params,
        )

        calc_func_params = calc_rule.calc_func_params if calc_rule.calc_func_params else {}

        return FuncCalcResultLogViewModel(
            func=calc_rule.calc_func.lower(),
            func_args=calc_func_params | {"pre_result": pre_result},
            calc_result=calc_result,
        )

    @staticmethod
    def assign(
        pre_result: List[CalcResultViewModel],
        args: Optional[Any],
    ) -> List[CalcResultViewModel]:
        """
        assign 计算方法
        :param pre_result:
        :param args:
        :return:
        """

        res_result_list = []

        score = args.get("score", None)

        if score is None:
            raise BusinessError("assign 计算方法 score 不能为空")

        for res in pre_result:
            res_result_list.append(res.cast_to(CalcResultViewModel, calc_result=score))

        return res_result_list

    @staticmethod
    def initialize(
        pre_result: List[CalcResultViewModel],
        args: Optional[Any],
    ) -> List[CalcResultViewModel]:
        """
        初始化 计算方法
        :param pre_result:
        :param args:
        :return:
        """

        res_result_list = []

        score = args.get("score", None)

        if score is None:
            raise BusinessError("initialize 计算方法 score 不能为空")

        for res in pre_result:
            if not res.calc_result or res.calc_result.get("score", None) is None:
                raise BusinessError("initialize 计算方法 前置结果 不能为空")
            res_score = res.calc_result.get("score", 0) * -1
            calc_result = float(Decimal(str(res_score)) + Decimal(str(score)))
            res_result_list.append(res.cast_to(CalcResultViewModel, calc_result=calc_result))

        return res_result_list

    @staticmethod
    def sum(
        pre_result: List[CalcResultViewModel],
        args: Optional[Any],
    ) -> List[CalcResultViewModel]:
        """
        sum 计算方法
        :param pre_result:
        :param args:
        :return:
        """

        res_result_list = []

        score = args.get("score", None)

        if score is None:
            raise BusinessError("initialize 计算方法 score 不能为空")

        for res in pre_result:
            if not res.calc_result or res.calc_result.get("score", None) is None:
                raise BusinessError("initialize 计算方法 前置结果 不能为空")
            calc_result = Decimal("0")
            for result in res.calc_result:
                if result is None:
                    raise BusinessError("initialize 计算方法 前置结果中不能存在空值")
                calc_result += Decimal(str(result))
            res_result_list.append(res.cast_to(CalcResultViewModel, calc_result=float(calc_result)))

        return res_result_list

    @staticmethod
    def weighting(
        pre_result: List[CalcResultViewModel],
        args: Optional[Any],
    ) -> Optional[float]:
        """
        权重 计算方法
        :param pre_result:
        :param args:
        :return:
        """

        pass
