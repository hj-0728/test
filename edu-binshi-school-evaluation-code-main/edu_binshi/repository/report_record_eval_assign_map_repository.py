from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from edu_binshi.entity.report_record_eval_assign_map import \
    ReportRecordEvalAssignMapEntity
from edu_binshi.model.report_record_eval_assign_map_model import \
    ReportRecordEvalAssignMapModel


class ReportRecordEvalAssignMapRepository(BasicRepository):
    """
    报告记录评价分配map repository
    """

    def insert_report_record_eval_assign_map(
        self,
        report_record_eval_assign_map: ReportRecordEvalAssignMapModel,
        transaction: Transaction,
    ):
        """
        添加 报告记录评价分配map
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=ReportRecordEvalAssignMapEntity,
            entity_model=report_record_eval_assign_map,
            transaction=transaction
        )
