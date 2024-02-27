from enum import Enum


class EnumUserCategory(str, Enum):
    USER = "用户"
    DINGTALK_USER = "钉钉用户"
    DINGTALK_K12_PARENT = "钉钉家长"
    WECOM_USER = "企业微信用户"
    WECOM_k12_PARENT = "企业微信家长"
