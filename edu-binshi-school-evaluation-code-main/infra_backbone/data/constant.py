from typing import Final


class SymbolConst:
    """
    符号常量
    """

    COLON: Final[str] = ":"


class RedisConst:
    """
    redis常量
    """

    SESSION: Final[str] = "SESSION"


class SchedulerJobConst:
    """
    定时任务相关常量
    """

    CHANNEL_SCHEDULER = "channel_scheduler"
    COMMAND_REFRESH = "refresh"


class OrganizationCodeConst:
    """
    组织code常量
    """

    # 滨江实验小学
    BJSYXX = "BJSYXX"


class DimensionCodeConst:
    """
    维度code常量
    """

    # 钉钉家校维度
    DINGTALK_EDU = "DINGTALK_EDU"
    DINGTALK_INNER = "DINGTALK_INNER"
