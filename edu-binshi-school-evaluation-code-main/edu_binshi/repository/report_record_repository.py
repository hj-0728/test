from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from edu_binshi.entity.report_record import ReportRecordEntity
from edu_binshi.model.report_record_model import ReportRecordModel


class ReportRecordRepository(BasicRepository):
    """
    报告记录 repository
    """

    def insert_report_record(
        self,
        report_record: ReportRecordModel,
        transaction: Transaction,
    ):
        """
        添加word表格样式配置
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=ReportRecordEntity, entity_model=report_record, transaction=transaction
        )

    def update_report_record(
        self,
        report_record: ReportRecordModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新word表格样式配置
        """
        return self._update_versioned_entity_by_model(
            entity_cls=ReportRecordEntity,
            update_model=report_record,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_report_record(
        self,
        report_record_id: str,
        transaction: Transaction,
    ):
        """
        删除word表格样式配置
        """
        return self._delete_versioned_entity_by_id(
            entity_cls=ReportRecordEntity,
            entity_id=report_record_id,
            transaction=transaction,
        )
