from enum import Enum


class EnumDingtalkUserCategory(Enum):
    """
    钉钉用户类型
    """

    DINGTALK_USER = "钉钉用户"
    DINGTALK_K12_PARENT = "钉钉k12家长"


class EnumTagName(Enum):
    """
    标签名称
    """
    CONSTANT = "N（常量）"
    VARIABLE = "X（变量）"


class EnumRedisFlag(Enum):
    """
    redis标记
    """
    FLAG_SAVE_BENCHMARK_SCORE = "保存得分日志的灯"
    FLAG_REGENERATE_SCORE_LOG = "生成分数日志"
    FLAG_HANDLE_GENERATE_INPUT_SCORE_LOG = "生成输入分数日志"
    FLAG_REFRESH_EVALUATION_CRITERIA_PLAN_DATA = "刷新评价标准计划数据"
    FLAG_SAVE_EVALUATION_ASSIGNMENT_RELATIONSHIP = "保存评价分配关系"
