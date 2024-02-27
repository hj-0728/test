from typing import List

from pydantic import BaseSettings, Field


class FlaskSetting(BaseSettings):
    app_name: str = Field(default="FLASK_APP", env="FLASK_APP_NAME")
    log_level: str = Field(default="DEBUG", env="FLASK_LOG_LEVEL")
    profiling: bool = Field(default=False, env="FLASK_PROFILING")
    secret_key: str = Field(default="!@#$%^&*()", env="FLASK_SECRET_KEY")
    static_folder: str = Field(default="static", env="FLASK_STATIC_FOLDER")
    template_folder: str = Field(default="templates", env="FLASK_TEMPLATE_FOLDER")
    app_url: str = Field(default="templates", env="FLASK_APP_URL")


class JwtSetting(BaseSettings):
    secret_key: str = Field(default="!@#$%^&*()", env="JWT_SECRET_KEY")
    access_token_expires: int = Field(default=900, env="JWT_ACCESS_TOKEN_EXPIRES")
    refresh_token_expires: int = Field(default=259200, env="JWT_REFRESH_TOKEN_EXPIRES")

    blacklist_enabled: bool = Field(default=False, env="JWT_BLACKLIST_ENABLED")
    redis_blocklist = Field(default="redis::redis@127.0.0.1:6379/0", env="JWT_REDIS_BLOCKLIST")

    token_location: List[str] = ["headers"]
    header_name: str = "Authorization"
    header_type: str = "Bearer"
    blacklist_token_checks: List[str] = ["access", "refresh"]


class DevSetting(BaseSettings):
    """
    开发配置（此项目是为了配置后端的space_id）
    代码里面经常有写死的organization_id、channel_id、people_id等(因为需要从nginx读或者需要身份验证)
    都不知道哪些地方被写死了，只有发现页面不对，去检查代码的时候才知道
    所以将这些参数放在配置文件统一管理
    """

    enabled: bool = Field(default=False, env="DEV_ENABLED")
    platform: str = Field(default="", env="DEV_PLATFORM")
    remote_user_id: str = Field(default="", env="DEV_REMOTE_USER_ID")
    dingtalk_corp_id: str = Field(default="", env="DEV_DINGTALK_CORP_ID")
    user_id: str = Field(default="", env="DEV_USER_ID")
    role_id: str = Field(default="", env="DEV_ROLE_ID")
    people_id: str = Field(default="", env="DEV_PEOPLE_ID")


class CelerySetting(BaseSettings):
    """
    Celery 配置信息
    """

    broker_url: str = Field(
        default="amqp://celery:celery@127.0.0.1:5672/celery", env="CELERY_BROKER_URL"
    )
    result_backend: str = Field(default=None, env="CELERY_RESULT_BACKEND")
    import_package: List[str] = Field(default=[], env="CELERY_IMPORT_PACKAGE")
