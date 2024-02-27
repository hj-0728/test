"""
钉钉用户 service
"""
from infra_basic.basic_repository import PageFilterParams

from infra_dingtalk.repository.dingtalk_user_repository import DingtalkUserRepository


class DingtalkUserService:
    def __init__(self, dingtalk_user_repository: DingtalkUserRepository):
        self._dingtalk_user_repository = dingtalk_user_repository

    def get_dingtalk_user_list(
        self,
        query_params: PageFilterParams,
        dingtalk_corp_id: str = None,
    ):
        """
        获取k12部门列表
        """
        return self._dingtalk_user_repository.get_dingtalk_user_by_dingtalk_corp_id(
            query_params=query_params,
            dingtalk_corp_id=dingtalk_corp_id,
        )
