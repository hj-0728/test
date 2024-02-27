# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from typing import Optional
from infra_dingtalk.dingtalk.client.api.base import DingTalkBaseAPI
from infra_basic.errors import BusinessError


class User(DingTalkBaseAPI):
    def auth_scopes(self):
        """
        获取CorpSecret授权范围

        :return:
        """
        return self._get("/auth/scopes")

    def get_user_count(self, only_active):
        """
        获取企业员工人数

        :param only_active: 是否包含未激活钉钉的人员数量
        :return: 企业员工数量
        """
        return self._post(
            "/topapi/user/count",
            {"onlyActive": 0 if only_active else 1},
            result_processor=lambda x: x["count"],
        )

    def get_user_info(self, code):
        """
        通过CODE换取用户身份

        :param code: requestAuthCode接口中获取的CODE
        :return:
        """
        return self._post(
            "/topapi/v2/user/getuserinfo", {"code": code}, result_processor=lambda x: x["result"]
        )

    def get(self, userid, lang="zh_CN"):
        """
        获取成员详情

        :param userid: 员工在企业内的UserID，企业用来唯一标识用户的字段
        :param lang: 通讯录语言(默认zh_CN，未来会支持en_US)
        :return:
        """
        return self._post(
            "/topapi/v2/user/get",
            {"userid": userid, "language": lang},
            result_processor=lambda x: x["result"],
        )

    def create(self, user_data):
        """
        创建成员

        :param user_data: 用户信息
        :return: userid
        """
        return self._post(
            "/topapi/v2/user/create", user_data, result_processor=lambda x: x["userid"]
        )

    def update(self, user_data):
        """
        更新成员

        :param user_data: 用户信息
        :return:
        """
        return self._post("/topapi/v2/user/update", user_data)

    def delete(self, userid):
        """
        删除成员

        :param userid: 员工在企业内的UserID，企业用来唯一标识用户的字段
        :return:
        """
        return self._post("/topapi/v2/user/delete", {"userid": userid})

    def batch_delete(self, user_ids):
        """
        批量删除成员

        :param user_ids: 员工UserID列表。列表长度在1到20之间
        :return:
        """
        return self._post("/user/delete", {"useridlist": list(user_ids)})

    def simple_list(self, department_id, offset=0, size=100, order="custom", lang="zh_CN"):
        """
        获取部门成员

        :param department_id: 获取的部门id
        :param offset: 偏移量
        :param size: 表分页大小，最大100
        :param order: 排序规则
                      entry_asc     代表按照进入部门的时间升序
                      entry_desc    代表按照进入部门的时间降序
                      modify_asc    代表按照部门信息修改时间升序
                      modify_desc   代表按照部门信息修改时间降序
                      custom        代表用户定义排序
        :param lang: 通讯录语言(默认zh_CN另外支持en_US)
        :return:
        """
        return self._get(
            "/user/simplelist",
            {
                "department_id": department_id,
                "offset": offset,
                "size": size,
                "order": order,
                "lang": lang,
            },
        )

    def list(
        self,
        dept_id: str,
        language: Optional[str] = None,
        contain_access_limit: bool = True,
        size: int = 30,
        cursor: int = 0,
        order_field: str = 'custom',
        user_list: list = [],
    ):
        """
        获取部门成员（详情）

        :param dept_id: 获取的部门id
        :param contain_access_limit: 是否返回访问受限的员工
        :param size: 表分页大小
        :param cursor:
        :param user_list: 表分页大小，最大100
        :param order_field: 排序规则
                      entry_asc     代表按照进入部门的时间升序
                      entry_desc    代表按照进入部门的时间降序
                      modify_asc    代表按照部门信息修改时间升序
                      modify_desc   代表按照部门信息修改时间降序
                      custom        代表用户定义排序
        :param language: 通讯录语言(默认zh_CN另外支持en_US)
        :return:
        """
        res = self._post(
            url="/topapi/v2/user/list",
            data={
                "dept_id": dept_id,
                "order_field": order_field,
                "contain_access_limit": contain_access_limit,
                "size": size,
                "cursor": cursor,
                "language": language,
            },
        )
        if res.get("errcode") != 0:
            raise BusinessError(
                "获取部门成员（详情）请求错误，errcode: {0}, request_id: {1}".format(res["errcode"], res["request_id"])
            )
        if not res["result"]["list"]:
            return user_list
        if res["result"]["has_more"]:
            user_list += self.list(dept_id=dept_id, size=size, cursor=res["result"]["next_cursor"], user_list=user_list)
        user_list = res["result"]["list"]
        return user_list

    def get_admin(self):
        """
        获取管理员列表

        :return: sys_level	管理员角色 1:主管理员,2:子管理员
        """
        return self._get("/user/get_admin", result_processor=lambda x: x["admin_list"])

    def can_access_microapp(self, app_id, user_id):
        """
        获取管理员的微应用管理权限

        :param app_id: 微应用id
        :param user_id: 员工唯一标识ID
        :return: 是否能管理该微应用
        """
        return self._get(
            "/user/can_access_microapp",
            {"appId": app_id, "userId": user_id},
            result_processor=lambda x: x["canAccess"],
        )

    def get_userid_by_unionid(self, unionid):
        """
        根据unionid获取成员的userid

        :param unionid: 用户在当前钉钉开放平台账号范围内的唯一标识
        :return:
        """
        return self._get("/user/getUseridByUnionid", {"unionid": unionid})

    def get_dept_member(self, dept_id):
        """
        获取部门用户userid列表

        :param dept_id: 用户在当前钉钉开放平台账号范围内的唯一标识
        :return 部门userid列表:
        """
        return self._get(
            "/topapi/user/listid",
            {"dept_id": dept_id},
            result_processor=lambda x: x["result"]["userid_list"],
        )

    def listbypage(self, department_id, offset=0, size=100, order="custom", lang="zh_CN"):
        """
        获取部门用户

        :param department_id: 获取的部门id
        :param offset: 偏移量
        :param size: 表分页大小，最大100
        :param order: 排序规则
                      entry_asc     代表按照进入部门的时间升序
                      entry_desc    代表按照进入部门的时间降序
                      modify_asc    代表按照部门信息修改时间升序
                      modify_desc   代表按照部门信息修改时间降序
                      custom        代表用户定义排序
        :param lang: 通讯录语言(默认zh_CN另外支持en_US)
        :return:
        """
        return self._get(
            "/user/list",
            {
                "department_id": department_id,
                "offset": offset,
                "size": size,
                "order": order,
                "lang": lang,
            },
        )

    def get_admin_scope(self, userid):
        """
        查询管理员通讯录权限范围

        :param userid: 用户id
        """
        return self._top_request(
            "dingtalk.oapi.user.get_admin_scope",
            {"userid": userid},
            result_processor=lambda x: x["dept_ids"],
        )
