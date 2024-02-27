from infra_backbone.model.access_log_model import AccessLogModel
from infra_backbone.repository.access_log_repository import AccessLogRepository


class AccessLogService:
    def __init__(self, access_log_repository: AccessLogRepository):
        self.__access_log_repository = access_log_repository

    def save_access_log(self, access_log: AccessLogModel):
        self.__access_log_repository.insert_access_log(data=access_log)
