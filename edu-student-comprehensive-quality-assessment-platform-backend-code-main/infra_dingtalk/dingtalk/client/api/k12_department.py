"""
钉钉k12部门相关API
"""

from typing import Dict, List, Optional

from infra_basic.errors import BusinessError

from infra_dingtalk.dingtalk.client.api.base import DingTalkBaseAPI


class K12Department(DingTalkBaseAPI):
    """
    k12部门相关api
    """

    def list(
        self,
        page_size: int = 30,
        page_no: int = 1,
        dept_list=None,
        super_id: Optional[int] = None,
    ):
        """
        递归，只能一层层获取k12部门, 木得办法  --tao.xia
        返回部门列表
        :params page_size: 1-30
        :page_no: 1 不填默认1
        """
        if dept_list is None:
            dept_list = []
        res = self._post(
            url="/topapi/edu/dept/list",
            data={
                "super_id": super_id,
                "page_size": page_size,
                "page_no": page_no,
            },
        )
        if not res.get("success"):
            raise BusinessError(
                "k12部门请求错误，errcode: {0}, request_id: {1}".format(res["errcode"], res["request_id"])
            )
        if not res["result"]["details"]:
            return dept_list
        if res["result"]["has_more"]:
            dept_list = self.list(page_no=page_no + 1, dept_list=dept_list)
        for dept in res["result"]["details"]:
            dept["parentid"] = super_id if super_id else 0
            dept_list.append(dept)
            dept_list = self.list(page_no=1, super_id=dept["dept_id"], dept_list=dept_list)
        return dept_list
