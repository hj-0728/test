"""
同步应用插件
"""

import ast
from typing import Dict, List

from infra_dingtalk.agent_plugin.base_plugin import DingtalkAgentBasePlugin
from infra_dingtalk.data.agent_plugin.dingtalk_dept import DingtalkDept
from infra_dingtalk.data.agent_plugin.dingtalk_user import DingtalkUser


class SyncAgentPlugin(DingtalkAgentBasePlugin):
    """
    同步应用插件
    """

    def get_all_user(self) -> Dict[str, DingtalkUser]:
        """
        获取所有用户
        :return: 返回部门字典，字典的键是用户id，值是用户详细信息
        """

        user_list = self._client.user.list(department_id=1, fetch_child=True)
        return {x["userid"]: DingtalkUser(**x) for x in user_list}

    def get_dd_user_list(self, remote_dept_ids: List[int]) -> Dict[str, DingtalkUser]:
        """
        获取钉钉人员
        @return:
        """
        dd_user_dict = {}
        for remote_dept_id in remote_dept_ids:
            dd_user_info_list = self._client.user.list(dept_id=remote_dept_id)
            for dd_user_info in dd_user_info_list:
                if not dd_user_dict.get(dd_user_info["userid"]):
                    dd_user = DingtalkUser(**dd_user_info)
                    dd_user.department = list(
                        set(remote_dept_ids).intersection(set(dd_user_info["dept_id_list"]))
                    )
                    dd_user.is_leader_in_dept = [remote_dept_id] if dd_user_info["leader"] else []
                    dd_user_dict[dd_user.userid] = dd_user
                else:
                    if dd_user_info["leader"]:
                        dd_user_dict.get(dd_user_info["userid"]).is_leader_in_dept.append(remote_dept_id)
        return dd_user_dict

    def get_all_dd_dept(self, result: List = None, _id: int = 1):
        """
        获取钉钉部门详细信息（除家校通讯录）  递归（钉钉递归获取部门信息不全）
        @return:
        """
        if result is None:
            result = []
        dept_info = self._client.department.get(_id=_id)
        if dept_info["dept_id"] == 1:
            dept_info["parent_id"] = 0
        result.append(dept_info)
        child_dept_list = self._client.department.list_ids(_id=_id)
        if child_dept_list:
            for child_dept_id in child_dept_list:
                if child_dept_id > 0:  # 家校通讯录的dept_id 为 负值（-7）
                    self.get_all_dd_dept(result=result, _id=child_dept_id)
        return self.__prepare_dept_level(result)

    def get_all_dept(self) -> Dict[int, DingtalkDept]:
        """
        获取所有部门
        :return: 返回部门字典，字典的键是部门id，值是部门详细信息
        """

        res = self._client.department.list()
        return self.__prepare_dept_level(dept_list=res)

    def __prepare_dept_level(
        self, dept_list: List[Dict], dept_id: int = 1
    ) -> Dict[int, DingtalkDept]:
        """
        准备部门的的层级信息
        :param dept_list:
        :return:
        """
        result = []
        top_node = self._find_dept_by_id(dept_list=dept_list, dept_id=dept_id)
        top_node["level"] = 1
        result.append(top_node)
        self._find_dept_child(dept_list=dept_list, parent_id=top_node["dept_id"], result=result)
        result.sort(key=lambda x: x["level"])
        return {x["dept_id"]: DingtalkDept(**x) for x in result}
