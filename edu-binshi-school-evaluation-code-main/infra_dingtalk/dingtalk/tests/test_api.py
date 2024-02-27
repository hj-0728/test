"""
钉钉应用插件
"""
from typing import Dict, List

from infra_basic.errors.input import DataNotFoundError
from redis import Redis

from infra_dingtalk.agent_plugin.ext_dingtalk_client import ExtDingtalkClient
from infra_dingtalk.data.agent_plugin.setup_options import AgentPluginSetupOptions
from infra_dingtalk.dingtalk.storage.kvstorage import KvStorage


class DingtalkAgentBasePlugin:
    """
    钉钉应用插件
    """

    def __init__(self, setup_options: AgentPluginSetupOptions):
        self._options = setup_options
        self.__init_agent_client()

    def __init_agent_client(self):
        """
        初始化
        :return:
        """
        session_interface = None
        if self._options.redis_url:
            redis_client = Redis.from_url(self._options.redis_url)
            session_interface = KvStorage(
                redis_client,
                prefix="dingtalk:{0}".format(self._options.app_secret),
            )
        self._client = ExtDingtalkClient(
            corp_id=self._options.corp_id,
            app_secret=self._options.app_secret,
            app_key=self._options.app_key,
            storage=session_interface,
        )


def test_department_api():
    """
    测试接口
    """
    plugin = DingtalkAgentBasePlugin(
        setup_options=AgentPluginSetupOptions(
            corp_id="ding59671a103ffc8e344ac5d6980864d335",
            app_secret="VBcbx9OJOkxmrKr6nKt05_YBJYVrT2z7Bja4tMrysu-LasyHEp0ffu9S7msEEP5v",
            app_key="dingvhjoxjuky063hfrz",
            agent_id="2627156980",
        )
    )
    client = plugin._client
    dept_list = client.department.list()
    dept_info = client.department.get(_id=414470359)
    list_parent_by_dept = client.department.list_parent_dept_by_dept(_id=488722923)
    print(dept_list)


def test_user_api():
    """
    测试用户接口
    """
    plugin = DingtalkAgentBasePlugin(
        setup_options=AgentPluginSetupOptions(
            corp_id="ding59671a103ffc8e344ac5d6980864d335",
            app_secret="VBcbx9OJOkxmrKr6nKt05_YBJYVrT2z7Bja4tMrysu-LasyHEp0ffu9S7msEEP5v",
            app_key="dingvhjoxjuky063hfrz",
            agent_id="2627156980",
        )
    )
    client = plugin._client
    user_info = client.user.get(userid="4707060359774889")
    dept_info = client.department.get(_id=488722923)
    list_parent_by_dept = client.department.list_parent_dept_by_dept(_id=488722923)
    print(user_info)


# 测试k12用户接口
def test_k12_user_api():
    """
    测试k12用户接口
    """
    plugin = DingtalkAgentBasePlugin(
        setup_options=AgentPluginSetupOptions(
            corp_id="ding59671a103ffc8e344ac5d6980864d335",
            app_secert="VBcbx9OJOkxmrKr6nKt05_YBJYVrT2z7Bja4tMrysu-LasyHEp0ffu9S7msEEP5v",
            app_key="dingvhjoxjuky063hfrz",
            agent_id="2627156980",
        )
    )
    client = plugin._client
    k12_user = client.k12_student.get(userid="4707060359774889")


# 二分查找
def binary_search(arr: List, target: int) -> int:
    """
    二分查找
    :param arr:
    :param target:
    :return:
    """
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) >> 1
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            right = mid - 1
        elif arr[mid] < target:
            left = mid + 1
    return -1
