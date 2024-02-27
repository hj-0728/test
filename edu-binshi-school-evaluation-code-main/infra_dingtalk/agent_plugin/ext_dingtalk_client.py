"""
dingtalk client扩展
"""
from infra_dingtalk.agent_plugin.ext_k12_api.dept import K12Dept
from infra_dingtalk.agent_plugin.ext_k12_api.student import K12User
from infra_dingtalk.dingtalk.client import AppKeyClient


class ExtDingtalkClient(AppKeyClient):
    """
    dingtalk client扩展
    """

    k12_dept = K12Dept()
    k12_user = K12User()
