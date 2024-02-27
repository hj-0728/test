from infra_basic.transaction import Transaction

from edu_binshi.model.report_record_model import ReportRecordModel
from edu_binshi.repository.report_record_repository import ReportRecordRepository


class ReportRecordService:
    """
    报告记录 service
    """

    def __init__(
            self,
            report_record_repository: ReportRecordRepository,
    ):
        self.__report_record_repository = report_record_repository

    def insert_report_record(
            self,
            report_record: ReportRecordModel,
            transaction: Transaction,
    ):
        """
        保存报告记录
        :return:
        """
        return self.__report_record_repository.insert_report_record(
            report_record=report_record,
            transaction=transaction,
        )
