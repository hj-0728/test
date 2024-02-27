from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier
from infra_utility.string_helper import is_not_blank
from loguru import logger

from backend.backend_containers import BackendContainer
from backend.data.constant import FlaskConfigConst
from backend.service.authorization_service import AuthorizationService

blueprint_oauth = Blueprint(
    name="oauth",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

DINGTALK_PREFIX = "/dingtalk/auth"


@blueprint_oauth.route(f"{DINGTALK_PREFIX}/dingtalk-login", methods=["POST"])
@inject
def route_dingtalk_oauth_login(
    authorization_service: AuthorizationService = Provide[BackendContainer.authorization_service],
):
    """
    dingtalk oauth2 登录
    """
    carrier = MessageCarrier()
    try:
        code = request.args.get("code")
        logger.info(f"身份验证code值【{code}")
        if is_not_blank(code):
            data = authorization_service.get_dingtalk_oauth_jwt_token(code=code)
            carrier.push_succeed_data(data=data)
            return jsonify(carrier.dict())
        # url = authorization_service.get_dingtalk_oauth_redirect_url(redirect_uri=request.referrer)
        # logger.info(f"身份验证url值【{url}】")

        carrier.push_redirect_url(redirect_url=request.referrer, code=302)
    except Exception as error:
        carrier.push_exception(error)
    logger.debug(f"身份验证carrier值【{ carrier.dict()}】")
    return jsonify(carrier.dict())
