from edu_binshi.repository.period_category_repository import PeriodCategoryRepository


class PeriodCategoryService:
    def __init__(
        self,
        period_category_repository: PeriodCategoryRepository,
    ):
        self.__period_category_repository = period_category_repository

    def get_period_category_list(
        self,
    ):
        """
        获取周期类型列表
        :return:
        """
        return self.__period_category_repository.get_period_category_list()
