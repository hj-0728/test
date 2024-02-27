from infra_basic.errors import BusinessError

from context_sync.repository.context_people_user_map_repository import (
    ContextPeopleUserMapRepository,
)


class ContextPeopleUserMapService:
    def __init__(self, context_people_user_map_repository: ContextPeopleUserMapRepository):
        self.__context_people_user_map_repository = context_people_user_map_repository

    def get_people_id_by_user_resource(self, res_id: str, res_category: str) -> str:
        """
        获取人员id
        @param res_id:
        @param res_category:
        @return:
        """
        context = self.__context_people_user_map_repository.fetch_context_people_by_user_resource(
            res_id=res_id,
            res_category=res_category,
        )
        if not context:
            raise BusinessError("未找到上下文人员")
        return context.people_id
