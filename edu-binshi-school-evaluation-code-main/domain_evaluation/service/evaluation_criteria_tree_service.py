from typing import List

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.algorithm.tree import list_to_tree
from infra_utility.datetime_helper import local_now

from domain_evaluation.data.enum import EnumTagOwnerCategory, EnumTagOwnershipRelationship
from domain_evaluation.data.query_params.evaluation_criteria_tree_item_query_params import (
    EvaluationCriteriaBoundTagItemQueryParams,
    EvaluationCriteriaNotBoundTagItemQueryParams,
)
from domain_evaluation.model.edit.evaluation_criteria_tree_bind_tag_em import (
    EvaluationCriteriaTreeBindTagEditModel,
)
from domain_evaluation.model.evaluation_criteria_tree_model import SaveEvaluationCriteriaTreeModel
from domain_evaluation.model.evaluation_criteria_tree_node_model import (
    EvaluationCriteriaTreeNodeModel,
)
from domain_evaluation.repository.evaluation_criteria_repository import EvaluationCriteriaRepository
from domain_evaluation.repository.evaluation_criteria_tree_repository import (
    EvaluationCriteriaTreeRepository,
)
from domain_evaluation.repository.indicator_repository import IndicatorRepository
from domain_evaluation.service.benchmark_service import BenchmarkService
from domain_evaluation.service.evaluation_criteria_service import \
    EvaluationCriteriaService
from domain_evaluation.service.indicator_service import IndicatorService
from infra_backbone.model.edit.save_tag_em import (
    SaveTagEditModel,
    SaveTagOwnershipRelationshipEditModel,
)
from infra_backbone.model.tag_ownership_relationship_model import TagOwnershipRelationshipModel
from infra_backbone.repository.tag_repository import TagRepository
from infra_backbone.service.tag_service import TagService


class EvaluationCriteriaTreeService:
    """
    评价标准的树（对用户可以叫评价项） service
    """

    def __init__(
        self,
        evaluation_criteria_tree_repository: EvaluationCriteriaTreeRepository,
        indicator_service: IndicatorService,
        evaluation_criteria_service: EvaluationCriteriaService,
        indicator_repository: IndicatorRepository,
        tag_repository: TagRepository,
        benchmark_service: BenchmarkService,
        tag_service: TagService,
    ):
        self.__evaluation_criteria_tree_repository = evaluation_criteria_tree_repository
        self.__indicator_service = indicator_service
        self.__evaluation_criteria_service = evaluation_criteria_service
        self.__indicator_repository = indicator_repository
        self.__tag_repository = tag_repository
        self.__benchmark_service = benchmark_service
        self.__tag_service = tag_service

    def save_evaluation_criteria_tree(
        self,
        evaluation_criteria_tree: SaveEvaluationCriteriaTreeModel,
        transaction: Transaction,
    ):
        """
        保存评价标准树
        :param evaluation_criteria_tree:
        :param transaction:
        """

        self.__evaluation_criteria_service.judge_evaluation_criteria_can_update(
            evaluation_criteria_id=evaluation_criteria_tree.evaluation_criteria_id
        )

        evaluation_criteria_tree.indicator_id = self.__indicator_service.save_indicator(
            indicator=evaluation_criteria_tree.to_indicator_model(),
            transaction=transaction,
        )
        if not evaluation_criteria_tree.id:
            # 保存评价标准树
            max_seq = (
                self.__evaluation_criteria_tree_repository.get_evaluation_criteria_tree_max_seq(
                    evaluation_criteria_id=evaluation_criteria_tree.evaluation_criteria_id,
                    parent_indicator_id=evaluation_criteria_tree.parent_indicator_id,
                )
            )
            evaluation_criteria_tree.seq = max_seq + 1
            evaluation_criteria_tree.id = self.__evaluation_criteria_tree_repository.insert_evaluation_criteria_tree(
                evaluation_criteria_tree=evaluation_criteria_tree.to_evaluation_criteria_tree_model(),
                transaction=transaction,
            )

        self.update_evaluation_criteria_tree_tag(
            evaluation_criteria_tree=evaluation_criteria_tree,
            transaction=transaction,
        )

    def update_evaluation_criteria_tree_tag(
        self,
        evaluation_criteria_tree: SaveEvaluationCriteriaTreeModel,
        transaction: Transaction,
    ):
        """保存、编辑指标时更新标签"""

        need_add_tag_relationship_tree_id_list = []
        parent_evaluation_criteria_tree = self.__evaluation_criteria_tree_repository.get_evaluation_criteria_tree_by_indicator_id(
            indicator_id=evaluation_criteria_tree.parent_indicator_id
        )
        if not parent_evaluation_criteria_tree:
            return
        # 获取原来的当前节点的tag
        old_tag_ownership_info = self.__tag_repository.get_tag_ownership_relationship_by_resource(
            resource_category=EnumTagOwnerCategory.EVALUATION_CRITERIA_TREE.name,
            resource_id=evaluation_criteria_tree.id,
        )
        if not old_tag_ownership_info:
            evaluation_criteria_tree.tag_ownership_id = (
                parent_evaluation_criteria_tree.tag_ownership_id
            )
            need_add_tag_relationship_tree_id_list.append(evaluation_criteria_tree.id)
        for tree_id in need_add_tag_relationship_tree_id_list:
            self.__tag_repository.insert_tag_ownership_relationship(
                tag_ownership_rel=TagOwnershipRelationshipModel(
                    tag_ownership_id=evaluation_criteria_tree.tag_ownership_id,
                    resource_category=EnumTagOwnerCategory.EVALUATION_CRITERIA_TREE.name,
                    resource_id=tree_id,
                    relationship=EnumTagOwnershipRelationship.EVALUATION.name,
                ),
                transaction=transaction,
            )

    def delete_evaluation_criteria_tree(
        self,
        transaction: Transaction,
        evaluation_criteria_tree_list: List[SaveEvaluationCriteriaTreeModel],
        indicator_id: str = None,
    ):
        """
        删除评价标准树 finish_at
        需将st_evaluation_criteria_tree表中该指标及子指标、st_indicator自身、指标相关st_benchmark和st_benchmark_input_node都删除
        :param transaction:
        :param evaluation_criteria_tree_list:
        :param indicator_id:
        """
        min_level = min(evaluation_criteria_tree_list, key=lambda obj: obj.level).level
        children = self.__evaluation_criteria_tree_repository.get_evaluation_criteria_tree_children(
            indicator_id=indicator_id,
        )
        # 比较前端传来的树节点和数据库中的树节点数量是否一致
        if len(children) != len(evaluation_criteria_tree_list):
            raise BusinessError("当前节点或子节点数据已发生变化，请刷新页面后重试")
        children_indicator_id_version_dict = {}
        for child in children:
            children_indicator_id_version_dict[child.indicator_id] = child.indicator_version
        # 逐一比较前端传来的树节点和数据库中的树节点version是否一致
        for evaluation_criteria_tree in evaluation_criteria_tree_list:
            if evaluation_criteria_tree.indicator_id not in children_indicator_id_version_dict:
                raise BusinessError("当前节点或子节点数据已发生变化，请刷新页面后重试")
            if (
                evaluation_criteria_tree.indicator_version
                != children_indicator_id_version_dict[evaluation_criteria_tree.indicator_id]
            ):
                raise BusinessError("当前节点或子节点数据已发生变化，请刷新页面后重试")
        for evaluation_criteria_tree in evaluation_criteria_tree_list:
            evaluation_criteria_tree_model = (
                evaluation_criteria_tree.to_evaluation_criteria_tree_model()
            )
            evaluation_criteria_tree_model.finish_at = local_now()

            self.__evaluation_criteria_tree_repository.update_evaluation_criteria_tree(
                evaluation_criteria_tree=evaluation_criteria_tree_model,
                transaction=transaction,
                limited_col_list=["finish_at"],
            )
            indicator = evaluation_criteria_tree.to_indicator_model()
            indicator.is_activated = False
            self.__indicator_repository.update_indicator(
                indicator=indicator,
                transaction=transaction,
                limited_col_list=["is_activated"],
            )
            # 删除st_benchmark、st_benchmark_input_node
            self.__benchmark_service.finish_benchmark_by_indicator_id(
                indicator_id=indicator.id,
                transaction=transaction,
                need_check_as_parent_source=evaluation_criteria_tree.level == min_level,
            )

    def update_evaluation_criteria_tree_seq(
        self,
        transaction: Transaction,
        evaluation_criteria_tree_list: [SaveEvaluationCriteriaTreeModel],
        parent_indicator_id: str = None,
    ):
        """
        更新评价标准树排序 在st_evaluation_criteria_tree也做删除后重建
        :param transaction:
        :param evaluation_criteria_tree_list:
        """
        children = self.__evaluation_criteria_tree_repository.get_evaluation_criteria_tree_children(
            indicator_id=parent_indicator_id,
        )
        children_id_version_dict = {}
        children_indicator_id_version_dict = {}
        for child in children:
            children_id_version_dict[child.id] = child.version
            children_indicator_id_version_dict[child.id] = child.indicator_version
        # 逐一比较前端传来的树节点和数据库中的树节点version是否一致
        for evaluation_criteria_tree in evaluation_criteria_tree_list:
            if evaluation_criteria_tree.id not in children_id_version_dict:
                raise BusinessError("当前节点或子节点数据已发生变化，请刷新页面后重试")
            if (
                evaluation_criteria_tree.version
                != children_id_version_dict[evaluation_criteria_tree.id]
                or evaluation_criteria_tree.indicator_version
                != children_indicator_id_version_dict[evaluation_criteria_tree.id]
            ):
                raise BusinessError("当前节点或子节点数据已发生变化，请刷新页面后重试")
            evaluation_criteria_tree.finish_at = local_now()
            self.__evaluation_criteria_tree_repository.update_evaluation_criteria_tree(
                evaluation_criteria_tree=evaluation_criteria_tree,
                transaction=transaction,
                limited_col_list=["finish_at"],
            )
            self.__evaluation_criteria_tree_repository.insert_evaluation_criteria_tree(
                evaluation_criteria_tree=evaluation_criteria_tree.to_save_evaluation_criteria_tree_model(),
                transaction=transaction,
            )

    def get_evaluation_criteria_tree(self, evaluation_criteria_id: str):
        """
        获取评价标准树
        :param evaluation_criteria_id:
        :return:
        """

        evaluation_criteria_tree_list = (
            self.__evaluation_criteria_tree_repository.get_evaluation_criteria_tree(
                evaluation_criteria_id=evaluation_criteria_id
            )
        )
        return list_to_tree(
            original_list=evaluation_criteria_tree_list,
            tree_node_type=EvaluationCriteriaTreeNodeModel,
            id_attr="indicator_id",
            parent_id_attr="parent_indicator_id",
        )

    def get_evaluation_criteria_tree_detail(
        self,
        evaluation_criteria_tree_id: str,
    ):
        """
        获取评价标准树详情
        :param evaluation_criteria_tree_id:
        :return:
        """
        return self.__evaluation_criteria_tree_repository.fetch_evaluation_criteria_tree_detail(
            evaluation_criteria_tree_id=evaluation_criteria_tree_id,
        )

    def delete_evaluation_criteria_tree_by_evaluation_criteria_id(
        self,
        evaluation_criteria_id: str,
        transaction: Transaction,
    ):
        """
        根据评价标准id删除评价标准树
        :param evaluation_criteria_id:
        :param transaction:
        """
        evaluation_criteria_tree_list = self.__evaluation_criteria_tree_repository.get_evaluation_criteria_tree_by_evaluation_criteria_id(
            evaluation_criteria_id=evaluation_criteria_id,
        )
        for evaluation_criteria_tree in evaluation_criteria_tree_list:
            evaluation_criteria_tree.is_deleted = True
            self.__evaluation_criteria_tree_repository.delete_evaluation_criteria_tree(
                evaluation_criteria_tree_id=evaluation_criteria_tree.id,
                transaction=transaction,
            )

    def evaluation_criteria_tree_bind_tag(
        self,
        evaluation_criteria_tree_bind_tag_em: EvaluationCriteriaTreeBindTagEditModel,
        transaction: Transaction,
    ):
        """
        绑定标签
        :param evaluation_criteria_tree_bind_tag_em:
        :param transaction:
        :return:
        """

        self.__evaluation_criteria_service.judge_evaluation_criteria_can_update(
            evaluation_criteria_id=evaluation_criteria_tree_bind_tag_em.evaluation_criteria_id
        )

        to_bind_tag_item_list = self.__evaluation_criteria_tree_repository.get_all_child_tree_by_tree_id_list(
            evaluation_criteria_tree_id_list=evaluation_criteria_tree_bind_tag_em.evaluation_criteria_tree_id_list
        )
        tag_ownership_relationship_em_list = []
        for to_bind_tag_item in to_bind_tag_item_list:
            tag_ownership_relationship_em_list.append(
                SaveTagOwnershipRelationshipEditModel(
                    resource_id=to_bind_tag_item.id,
                    resource_category=EnumTagOwnerCategory.EVALUATION_CRITERIA_TREE.name,
                    relationship=EnumTagOwnershipRelationship.EVALUATION.name,
                )
            )
        self.__tag_service.save_tag_and_related_relationship(
            tag=SaveTagEditModel(
                name=evaluation_criteria_tree_bind_tag_em.tag_name,
                tag_ownership_relationship_list=tag_ownership_relationship_em_list,
            ),
            transaction=transaction,
        )

    def evaluation_criteria_tree_unbound_tag(
        self,
        evaluation_criteria_tree_bind_tag_em: EvaluationCriteriaTreeBindTagEditModel,
        transaction: Transaction,
    ):
        """
        解除绑定标签
        :param evaluation_criteria_tree_bind_tag_em:
        :param transaction:
        :return:
        """
        self.__evaluation_criteria_service.judge_evaluation_criteria_can_update(
            evaluation_criteria_id=evaluation_criteria_tree_bind_tag_em.evaluation_criteria_id
        )

        have_bind_tag_item_list = self.__evaluation_criteria_tree_repository.get_evaluation_criteria_tree_by_evaluation_criteria_id_and_tag_name(
            evaluation_criteria_tree_id_list=evaluation_criteria_tree_bind_tag_em.evaluation_criteria_tree_id_list,
            tag_name=evaluation_criteria_tree_bind_tag_em.tag_name,
        )

        for have_bind_tag_item in have_bind_tag_item_list:
            if have_bind_tag_item.tag_ownership_relationship_id:
                self.__tag_service.delete_tag_ownership_relationship(
                    tag_ownership_relationship_id=have_bind_tag_item.tag_ownership_relationship_id,
                    transaction=transaction,
                )

    def get_evaluation_criteria_tree_bound_tag_item_list(
        self, query_params: EvaluationCriteriaBoundTagItemQueryParams
    ):
        """
        获取评价标准树绑定的标签
        """
        return self.__evaluation_criteria_tree_repository.get_evaluation_criteria_tree_bound_tag_item_list(
            query_params=query_params
        )

    def get_evaluation_criteria_tree_bound_tag_detail(self, evaluation_criteria_id: str):
        """
        获取评价标准树绑定的标签详情
        """
        return self.__evaluation_criteria_tree_repository.get_evaluation_criteria_tree_bound_tag_detail(
            evaluation_criteria_id=evaluation_criteria_id
        )

    def get_evaluation_criteria_tree_not_bound_tag_item_list(
        self, query_params: EvaluationCriteriaNotBoundTagItemQueryParams
    ):
        """
        获取评价标准树未绑定标签的评价项
        """
        return self.__evaluation_criteria_tree_repository.get_evaluation_criteria_tree_not_bound_tag_item_list(
            query_params=query_params
        )
