"""
常量定义
"""

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
    VERIFY_LOGIN_IMAGE: Final[str] = "VERIFY_LOGIN_IMAGE"
    SESSION_ABILITY_PER: Final[str] = "SESSION_ABILITY_PER"
    USER: Final[str] = "USER"
    DD_USER: Final[str] = "DD_USER"
    PERIOD: Final[str] = "PERIOD"


class FlaskConfigConst:
    """
    flask的一些配置
    """

    API_PREFIX: Final[str] = "/api"
    IMAGE_VERIFICATION_CODE_VALIDITY_PERIOD: Final[int] = 60 * 60
