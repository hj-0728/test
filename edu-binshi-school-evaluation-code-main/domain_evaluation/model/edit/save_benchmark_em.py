from typing import Optional

from infra_basic.basic_model import BasePlusModel

from domain_evaluation.data.enum import EnumResource, EnumTagOwnershipRelationship, EnumTagOwnerCategory
from domain_evaluation.model.benchmark_model import BenchmarkModel
from infra_backbone.model.edit.save_tag_em import SaveTagEditModel
from infra_backbone.model.tag_ownership_relationship_model import TagOwnershipRelationshipModel


class SaveBenchmarkEditModel(BasePlusModel):
    benchmark: BenchmarkModel

    tag_id: Optional[str]
    tag_name: Optional[str]

    tag_ownership_id: Optional[str]
    evaluation_criteria_id: Optional[str]

    def build_save_tag_em(self, benchmark_id: str) -> SaveTagEditModel:
        """
        组建SaveTagEditModel
        """
        rel = {
            "resource_category": EnumResource.BENCHMARK.name,
            "resource_id": benchmark_id,
            "relationship": EnumTagOwnershipRelationship.EVALUATION.name,
        }
        return SaveTagEditModel(
            id=self.tag_id, name=self.tag_name, tag_ownership_relationship_list=[rel]
        )

    def build_save_tag_ownership_relationship_model(self, benchmark_id: str) -> TagOwnershipRelationshipModel:
        """
        组建TagOwnershipRelationshipModel
        """
        return TagOwnershipRelationshipModel(
            tag_ownership_id=self.tag_ownership_id,
            resource_category=EnumTagOwnerCategory.BENCHMARK.name,
            resource_id=benchmark_id,
            relationship=EnumTagOwnershipRelationship.EVALUATION.name,
        )
