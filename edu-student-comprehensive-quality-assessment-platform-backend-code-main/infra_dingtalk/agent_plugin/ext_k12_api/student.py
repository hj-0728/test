"""
钉钉k12用户相关API
"""

from typing import Dict, List, Optional

from dingtalk.client.api.base import DingTalkBaseAPI
from infra_basic.errors import BusinessError


class K12User(DingTalkBaseAPI):
    """
    钉钉k12用户相关API
    """

    def get(self) -> List[Dict]:
        """
        获取所有用户
        """
        params = {"department_id": 1, "fetch_child": 1}
        return self._get("school/user/list", params=params)["students"]

    def list(
        self,
        role: str,
        user_list: List[Dict],
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
        if not res["result"]["details"]:
            return user_list
        if res["result"]["has_more"]:
            user_list = self.list(
                page_no=page_no + 1, user_list=user_list, class_id=class_id, role=role
            )
        for user in res["result"]["details"]:
            if role == "student":
                user["parents"] = []
            user_list.append(user)
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
        if not res.get("success"):
            raise BusinessError(
                "监护人{0}请求错误，errcode: {1}, request_id: {1}".format(
                    user_id, res["errcode"], res["request_id"]
                )
            )
        return res["result"]["relations"]
