from typing import Optional, List

from infra_basic.basic_repository import BasicRepository
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import PageInitParams, OrderCondition
from infra_basic.transaction import Transaction

from domain_evaluation.data.query_params.todo_task_query_params import \
    TodoTaskQueryParams
from domain_evaluation.entity.todo_task import TodoTaskEntity
from domain_evaluation.model.edit.save_todo_task_em import SaveTodoTaskEditModel
from domain_evaluation.model.todo_task_model import TodoTaskModel, \
    EnumTodoTaskTriggerCategory
from domain_evaluation.model.view.todo_task_page_vm import TodoTaskPageViewModel


class TodoTaskRepository(BasicRepository):
    """
    待办事项 Repository
    """

    def insert_todo_task(
        self,
        todo_task: TodoTaskModel,
        transaction: Transaction,
    ) -> str:
        """
        插入待办事项
        :param todo_task:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=TodoTaskEntity, entity_model=todo_task, transaction=transaction
        )

    def update_todo_task(
        self,
        todo_task: TodoTaskModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        修改待办事项
        :param todo_task:
        :param transaction:
        :param limited_col_list:
        :return:
        """

        return self._update_versioned_entity_by_model(
            entity_cls=TodoTaskEntity,
            update_model=todo_task,
            transaction=transaction,
            limited_col_list=limited_col_list
        )

    def fetch_todo_task_page(
        self, params: TodoTaskQueryParams
    ) -> PaginationCarrier[TodoTaskPageViewModel]:
        """
        先默认只有plan
        :param params:
        :return:
        """

        sql = """
        select tt.*, cp.name as plan_name,
        COALESCE(p.name,u.name) as completed_people_name
        from st_todo_task tt 
        inner join st_evaluation_criteria_plan cp on cp.id=tt.trigger_id
        left join st_user u on u.id=tt.completed_by
        left join st_people_user pu on pu.user_id=u.id
        left join st_people p on p.id=pu.people_id
        and trigger_category=:trigger_category
        where true
        """

        if params.period_id:
            sql += " and cp.focus_period_id=:period_id "

        if params.is_completed:
            sql += " and tt.completed_at is not null"

        elif params.is_completed is not None:
            sql += " and tt.completed_at is null"

        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["name"],
            order_columns=[OrderCondition(
                column_name="completed_at",
                order="desc",
            ), OrderCondition(
                column_name="generated_at",
                order="desc",
            )],
            params={
                "trigger_category": EnumTodoTaskTriggerCategory.EVALUATION_CRITERIA_PLAN.name,
                "period_id": params.period_id,
            },
        )
        return self._paginate(
            result_type=TodoTaskPageViewModel,
            total_params=page_init_params,
            page_params=params,
        )

    def fetch_existed_todo_task(self, params: SaveTodoTaskEditModel) -> List[str]:
        """
        获取已存在的待办事项
        """
        sql = """
        select * from st_todo_task
        where completed_by is null and title = any(array[:title_list])
        and assign_category = :assign_category and assign_id = :assign_id
        and trigger_category = :trigger_category and trigger_id = :trigger_id
        """
        data = self._execute_sql(
            sql=sql, params=params.dict()
        )
        return [x["title"] for x in data]
