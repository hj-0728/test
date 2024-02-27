from typing import Final


class FlaskConfigConst:
    """
    用于存储 Flask 应用的一些配置信息。
    """
    API_PREFIX: Final[str] = "/api"
# 类变量API_PREFIX被注解为Final[str]表示这是一个不可变的字符串常量，它的值为 "/api"，
# 用于定义 API 的前缀。

class AppRedisConst:#类中定义多个变量，每个变量都被注解为final类型
    SESSION: Final[str] = "SESSION"
    SESSION_ROLE: Final[str] = "SESSION_ROLE"
    VERIFY_LOGIN_IMAGE: Final[str] = "VERIFY_LOGIN_IMAGE"
    SESSION_ABILITY_PER: Final[str] = "SESSION_ABILITY_PER"
    DINGTALK_USER: Final[str] = "DINGTALK_USER"
    USER: Final[str] = "USER"
    CURRENT_SEMESTER_PERIOD: Final[str] = "CURRENT_SEMESTER_PERIOD"
    ROBOT_HANDLER: Final[str]        = "ROBOT_HANDLER"
    IMAGE_VERIFICATION_CODE_VALIDITY_PERIOD: Final[int] = 60 * 60


class PubsubConfigConst:
    """
    pubsub的一些配置
    """

    MAX_RETRIES: Final[int] = 3#不可变整数常量


class BusinessConst:
    """
    业务常量
    """

    SEARCH_HISTORY_LIMIT_COUNT: Final[int] = 10
    # 定义搜索历史记录的最大数量限制。
