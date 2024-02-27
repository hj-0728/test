import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork
from loguru import logger

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_handler
from backend.data.constant import FlaskConfigConst
from infra_backbone.service.storage_service import StorageService

blueprint_storage = Blueprint(
    name="storage", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

MOBILE_PREFIX = "/mobile/storage"
WEB_PREFIX = "/web/storage"


@blueprint_storage.route(f"{WEB_PREFIX}/upload-files", methods=["POST"])
@blueprint_storage.route(f"{MOBILE_PREFIX}/upload-files", methods=["POST"])
@inject
def route_upload_files(
    storage_service: StorageService = Provide[BackendContainer.backbone_container.storage_service],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    上传文件
    :return:
    """
    carrier = MessageCarrier()
    files = request.files.getlist("files")
    try:
        if not files:
            raise BusinessError("未获取到上传的文件")

        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="upload_files",
        )
        with uow:
            file_info_list = storage_service.upload_files(
                file_list=files,
                transaction=transaction,
            )
        carrier.push_succeed_data(file_info_list)
    except BusinessError as err:
        logger.error(err)
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
