from infra_basic.errors import BusinessError

from infra_dingtalk.repository.dingtalk_corp_repository import DingtalkCorpRepository


class DingtalkCorpService:
    def __init__(self, dingtalk_corp_repository: DingtalkCorpRepository):
        self.__dingtalk_corp_repository = dingtalk_corp_repository

    def get_current_dingtalk_corp_id(self) -> str:
        """
        在一个项目下只会一个钉钉的场景里面写的
        所以默认返回第一个
        """
        dingtalk_corp_list = self.__dingtalk_corp_repository.get_dingtalk_corp()
        if not dingtalk_corp_list:
            raise BusinessError("未获取到钉钉")
        return dingtalk_corp_list[0].id
