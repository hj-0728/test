from enum import Enum


class EnumBenchmarkComponentType(Enum):
    SINGLE_CHOICE = "单选"
    DIGITAL_INPUT_AND_STATS = "数字输入后选择统计方法"
    RANGE_VALUE = "区间取值"


class EnumResource(Enum):
    ESTABLISHMENT_ASSIGN = "编制分配"
    TEAM = "小组"

    BENCHMARK = "基准"
    EVALUATION_CRITERIA_TREE = "评价标准树"


class EnumTagOwnerCategory(Enum):
    """
    标签所属者类型
    """

    BENCHMARK = "基准"
    EVALUATION_CRITERIA_TREE = "评价标准树"
    BENCHMARK_STRATEGY = "评价策略"


class EnumComponentType(Enum):
    SINGLE_CHOICE = "单选"
    MULTIPLE_CHOICE = "多选"
    INTEGER = "整数"
    NUMERIC_RANGE = "数字区间"
    WEIGHT = "权重"
    TREE_SELECT = "树选择"
    RANGE_VALUE = "区间取值"
    STATS_TREE = "统计树选择"
    STATS_CHOICE = "统计多选"


class EnumTagOwnershipRelationship(Enum):
    """
    标签所有权关系
    """

    EVALUATION = "评价"
