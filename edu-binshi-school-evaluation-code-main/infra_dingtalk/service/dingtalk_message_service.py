import logging

from infra_basic.errors import BusinessError
from infra_utility.string_helper import is_not_blank
from wechatpy.exceptions import WeChatClientException

from infra_dingtalk.model.dingtalk_agent_model import EnumDingtalkAgent
from infra_dingtalk.repository.dingtalk_agent_repository import DingtalkAgentRepository
from infra_dingtalk.service.plugin_service import PluginService


class DingtalkMessageService:
    def __init__(
        self,
        plugin_service: PluginService,
        dingtalk_agent_repository: DingtalkAgentRepository,
    ):
        self._plugin_service = plugin_service
        self._dingtalk_agent_repository = dingtalk_agent_repository

    def send_message_to_dingtalk_users(
        self,
        dingtalk_corp_id: str,
        dingtalk_user_ids: list,
        title: str,
        description: str,
        url: str = None,
    ):
        message_delivery_agent = self._dingtalk_agent_repository.fetch_dingtalk_agent(
            dingtalk_corp_id=dingtalk_corp_id, code=EnumDingtalkAgent.MESSAGE_DELIVERY.name
        )
        if not message_delivery_agent:
            raise BusinessError("未找到钉钉应用[{0}]".format(EnumDingtalkAgent.MESSAGE_DELIVERY.name))
        try:
            dingtalk_helper = self._plugin_service.get_message_delivery_plugin_instance_in_app(
                dingtalk_corp_id=dingtalk_corp_id
            )
            if url and is_not_blank(url):
                dingtalk_helper.send_text_card(
                    agent_id=message_delivery_agent.remote_agent_id,
                    user_ids=dingtalk_user_ids,
                    title=title,
                    description=description,
                    url=url,
                )
            else:
                text_content = "{0}\n{1}".format(title, description)
                dingtalk_helper.send_text(
                    agent_id=message_delivery_agent.remote_agent_id,
                    user_ids=dingtalk_user_ids,
                    content=text_content,
                )
            error_code = 0
            status = "SUCCESS"
            err_message = None
        except WeChatClientException as e:
            error_code = e.errcode
            status = "FAILED"
            err_message = "应用[{0}]发送微信消息给[{1}]失败:{2}".format(
                message_delivery_agent.code, description, str(e)
            )
            err_message = err_message
            # 发送微信消息，如果应用无法发到任何人的话，就会失败抛出错误
            logging.error(err_message)
        return {"status": status, "error_code": error_code, "err_message": err_message}
