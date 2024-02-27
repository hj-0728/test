"""
k12同步应用插件
"""
import json
from typing import Dict, List

from infra_dingtalk.agent_plugin.base_plugin import DingtalkAgentBasePlugin
from infra_dingtalk.data.agent_plugin.dingtalk_k12_dept import DingtalkK12Dept
from infra_dingtalk.data.agent_plugin.dingtalk_student import DingtalkStudent


class K12SyncAgentPlugin(DingtalkAgentBasePlugin):
    """
    同步应用插件
    """

    def get_all_dept(self) -> Dict[int, DingtalkK12Dept]:
        """
        获取所有部门
        :return: 返回部门字典，字典的键是部门id，值是部门详细信息
        """
        res = self._client.k12_department.list()
        for dept in res:
            if dept["dept_type"] == "class":
                teacher_list = self._client.k12_user.list(
                    class_id=dept["dept_id"], role="teacher", user_list=[]
                )
                for teacher in teacher_list:
                    if json.loads(teacher["feature"]).get("is_adviser") == 1:
                        teacher["duty"] = "HEAD_TEACHER"
                    else:
                        teacher["duty"] = "TEACHER"
                dept["department_admins"] = teacher_list
        return {x["dept_id"]: DingtalkK12Dept(**x) for x in res}

    def __prepare_dept_level(
        self, dept_list: List[Dict], dept_id: int = 1
    ) -> Dict[int, DingtalkK12Dept]:
        """
        准备部门的的层级信息
        :param dept_list:
        :return:
        """
        result = []
        top_node = self._find_dept_by_id(dept_list=dept_list, dept_id=dept_id)
        top_node["level"] = 1
        result.append(top_node)
        self._find_dept_child(dept_list=dept_list, parent_id=top_node["id"], result=result)
        result.sort(key=lambda x: x["level"])
        return {x["id"]: DingtalkK12Dept(**x) for x in result}

    def get_all_student(self) -> Dict[str, DingtalkStudent]:
        """
        获取所有学生
        返回以学生id为键的字典
        """

        student = self._client.k12_user.get()
        return {x["student_userid"]: DingtalkStudent(**x) for x in student}

    def get_k12_student(self, class_id: int) -> List[Dict]:
        """
        获取所有的学生
        """
        student_list = self._client.k12_user.list(class_id=class_id, role="student", user_list=[])
        parent_list = self._client.k12_user.list(class_id=class_id, role="guardian", user_list=[])
        parent_result = []
        for parent in parent_list:
            relation_list = self._client.k12_user.guardian(
                class_id=class_id, user_id=parent["userid"]
            )
            for relation in relation_list:
                relation["unionid"] = parent["unionid"]
                parent_result.append(relation)
        for student in student_list:
            for parent in parent_result:
                if student["userid"] == parent["to_userid"]:
                    student["parents"].append(parent)
        return student_list
