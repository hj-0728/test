"""
钉钉k12用户相关API
"""

from typing import Dict, List, Optional

from infra_basic.errors import BusinessError

from infra_dingtalk.dingtalk.client.api.base import DingTalkBaseAPI


class K12User(DingTalkBaseAPI):
    """
    钉钉k12用户相关API
    """

    def teacher_list(self, page_size: int = 30, page_no: int = 1, class_id: Optional[int] = None):
        """
        获取老师列表
        """
        return self.list(role="teacher", page_size=page_size, page_no=page_no, class_id=class_id)

    def student_list(self, page_size: int = 30, page_no: int = 1, class_id: Optional[int] = None):
        """
        获取学生列表
        """
        return self.list(role="student", page_size=page_size, page_no=page_no, class_id=class_id)

    def guardian_list(self, page_size: int = 30, page_no: int = 1, class_id: Optional[int] = None):
        """
        监护人列表
        """
        return self.list(role="guardian", page_size=page_size, page_no=page_no, class_id=class_id)

    def list(
        self,
        role: str,
        user_list: List[Dict] = None,
        page_size: int = 30,
        page_no: int = 1,
        class_id: Optional[int] = None,
    ):
        """
        根据角色获取班级所有人员
        role: teacher：老师
              guardian：监护人
              student：用户
        """

        if user_list is None:
            user_list = []
        res = self._post(
            url="/topapi/edu/user/list",
            data={
                "class_id": class_id,
                "role": role,
                "page_size": page_size,
                "page_no": page_no,
            },
        )
        if not res.get("success"):
            raise BusinessError(
                "k12人员请求错误，errcode: {0}, request_id: {1}".format(res["errcode"], res["request_id"])
            )
        for user in res["result"]["details"]:
            if role == "student":
                user["parents"] = []
            user_list.append(user)
        if not res["result"]["details"]:
            return user_list
        if res["result"]["has_more"]:
            user_list = self.list(
                page_no=page_no + 1, page_size=page_size, user_list=user_list, class_id=class_id, role=role
            )
        return user_list

    def guardian(self, class_id: int, user_id: str):
        """
        监护人详情
        """
        res = self._post(
            url="/topapi/edu/user/relation/get",
            data={
                "class_id": class_id,
                "from_userid": user_id,
            },
        )
        guardian_user_res = self._post(
            "/topapi/v2/user/get",
            {"userid": user_id, "language": "zh_CN"},
            result_processor=lambda x: x["result"],
        )

        if not res.get("success"):
            raise BusinessError(
                "监护人{0}请求错误，errcode: {1}, request_id: {1}".format(
                    user_id, res["errcode"], res["request_id"]
                )
            )
        for relation in res["result"]["relations"]:
            relation["mobile"] = guardian_user_res.get("mobile")
        return res["result"]["relations"]
