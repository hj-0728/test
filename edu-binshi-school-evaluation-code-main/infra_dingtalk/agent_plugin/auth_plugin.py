"""
身份验证应用插件
"""
from typing import Dict, List

import six
from dingtalk.client.api.base import DingTalkBaseAPI
from optionaldict import optionaldict

from infra_dingtalk.agent_plugin.base_plugin import DingtalkAgentBasePlugin
from infra_dingtalk.data.agent_plugin.dingtalk_user_info import DingtalkUserInfo


class AuthAgentPlugin(DingtalkAgentBasePlugin, DingTalkBaseAPI):
    """
    身份验证应用插件
    """

    def get_user_info(self, code: str) -> DingtalkUserInfo:
        """
        根据code获取用户信息
        @param code:
        @return:
        """
        dingtalk_user_info = self._client.user.getuserinfo(code)
        return DingtalkUserInfo(**dingtalk_user_info)

    def get_authorize_url(self, redirect_uri: str) -> str:
        """
        生成钉钉认证后跳转的url
        :param redirect_uri:
        :return:
        """
        redirect_uri = six.moves.urllib.parse.quote(redirect_uri, safe=b"") if redirect_uri else ""
        url_list = [
            "https://oapi.dingtalk.com/connect/oauth2/sns_authorize?appid=",
            self._options.agent_id,
            "&response_type=code&scope=snsapi_auth&state=STATE&redirect_uri=",
            redirect_uri,
        ]
        return "".join(url_list)

    def send_text_card(
        self, agent_id: str, user_ids: List[str], title: str, description: str, url: str
    ) -> Dict:
        """
        发送text card类型消息
        @param agent_id:
        @param user_ids:
        @param title:
        @param description:
        @param url:
        @return:
        """
        msg_body = {
            "msgtype": "action_card",
            "action_card": {
                "title": title,
                "markdown": description,
                "single_title": "查看详情",
                "single_url": url,
            },
        }
        return self._client.message.send(agentid=agent_id, msg_body=msg_body, touser_list=user_ids)

    def send_text(self, agent_id: str, user_ids: List[str], content: str):
        """
        发送text类型消息
        @param agent_id:
        @param user_ids:
        @param content:
        @return:
        """
        msg_body = {
            "msgtype": "text",
            "text": {"content": content},
        }
        return self._client.message.send(agentid=agent_id, msg_body=msg_body, touser_list=user_ids)

    def send_text_to_parents(self, to_parent_user_ids: list, agent_id: str, message_dict: dict):
        data = optionaldict(
            to_parent_userid=to_parent_user_ids, msgtype="text", agentid=agent_id, text=message_dict
        )
        return self._post("externalcontact/message/send", data=data)
