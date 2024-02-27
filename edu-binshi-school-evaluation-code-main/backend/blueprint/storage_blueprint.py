import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier
from infra_object_storage.service.object_storage_service import ObjectStorageService

from backend.backend_containers import BackendContainer
from backend.data.constant import FlaskConfigConst
from backend.service.storage_service import StorageService
from backend.blueprint import get_current_user_role_handler
from infra_basic.errors import BusinessError
from infra_basic.uow_interface import UnitOfWork


blueprint_storage = Blueprint(
    name="storage",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/storage"


@blueprint_storage.route(f"{WEB_PREFIX}/get-file-url/<string:file_id>", methods=["GET"])
@inject
def route_get_file_download_url(
    file_id: str,
    object_storage_service: ObjectStorageService = Provide[
        BackendContainer.object_storage_container.object_storage_service,
    ],
) -> jsonify:
    """
    :return:
    """
    carrier = MessageCarrier()
    try:
        file_url = object_storage_service.get_file_url(
            file_id=file_id,
        )
        carrier.push_succeed_data(data=file_url)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))

@blueprint_storage.route(f"{WEB_PREFIX}/upload", methods=["POST"])
@inject
def route_upload_files(
    storage_service: StorageService = Provide[BackendContainer.storage_service,],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    上传文件
    :return:
    """
    carrier = MessageCarrier()
    files = request.files.getlist("files")
    file_uid_list_str = request.form.get("fileUidListStr", "")
    file_uid_list = [x for x in file_uid_list_str.split("&&&&")]
    try:
        if not files:
            raise BusinessError("未获取到上传的文件")

        transaction = uow.log_transaction(
            handler=get_current_user_role_handler(),
            action="upload_files",
        )
        with uow:
            file_info_list = storage_service.upload_files(
                file_list=files,
                transaction=transaction,
            )
        result = []
        for idx, file_info in enumerate(file_info_list):
            file_dict = file_info.dict()
            file_dict["uid"] = file_uid_list[idx]
            result.append(file_dict)
        carrier.push_succeed_data(result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict())
