from infra_basic.basic_model import VersionedModel


class DingtalkMessageDeliveryLogModel(VersionedModel):
    """
    钉钉消息递送日志
    """

    dingtalk_corp_id: str
    message_delivery_log_id: str
    error_code: str
    error_message: str
