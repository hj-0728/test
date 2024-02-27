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
