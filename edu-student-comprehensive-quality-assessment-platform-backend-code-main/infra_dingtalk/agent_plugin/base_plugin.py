"""
钉钉应用插件
"""
from typing import Dict, List

from infra_basic.errors.input import DataNotFoundError
from redis import Redis

from infra_dingtalk.data.agent_plugin.setup_options import AgentPluginSetupOptions
from infra_dingtalk.dingtalk.client import AppKeyClient
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
        self._client = AppKeyClient(
            corp_id=self._options.corp_id,
            app_secret=self._options.app_secret,
            app_key=self._options.app_key,
            storage=session_interface,
        )

    def get_client(self) -> AppKeyClient:
        """
        获取钉钉应用实例
        :return:
        """
        return self._client

    def get_options(self) -> AgentPluginSetupOptions:
        """
        获取钉钉应用初始化参数
        :return:
        """
        return self._options

    @staticmethod
    def _find_dept_by_id(dept_list: List[Dict], dept_id: int) -> Dict:
        """
        根据部门id找到部门信息
        :param dept_list: 部门列表
        :param dept_id: 部门id
        :return:
        """
        for dept in dept_list:
            if dept["dept_id"] == dept_id:
                return dept
        raise DataNotFoundError(f"id为【{dept_id}】的部门")

    def _find_dept_child(self, dept_list: List, parent_id: int, result: List[Dict]):
        """
        从列表中找到子级部门
        :param dept_list:
        :param parent_id:
        :param result:
        :return:
        """

        for child in dept_list:
            if child["parent_id"] == parent_id:
                parent = self._find_dept_by_id(dept_list=result, dept_id=parent_id)
                level = parent["level"] + 1
                child["level"] = level
                result.append(child)
                self._find_dept_child(
                    dept_list=dept_list,
                    parent_id=child["dept_id"],
                    result=result,
                )
