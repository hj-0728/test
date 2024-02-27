from pathlib import Path
from typing import Any, Callable, Dict

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from infra_basic.basic_resource import BasicResource
from infra_basic.uow_interface import UnitOfWork
from infra_utility.file_helper import build_abs_path_by_file
from infra_utility.lang_helper import scan_objects_from_module
from infra_utility.serialize_helper import ORJSONDecoder, ORJSONEncoder
from werkzeug.middleware.profiler import ProfilerMiddleware

from backend.backend_container import BackendContainer
from backend.data.settings import DevSetting, FlaskSetting, JwtSetting
from infra_backbone.service.robot_service import RobotService

# Json Web Tokens
jwt = JWTManager()


@inject
def load_system_robot(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
) -> BasicResource:
    with uow:
        robot = robot_service.get_system_robot().to_basic_handler()
    return robot


def create_flask_app(
    blueprint_module: Any = None,
    error_handler_func: Callable = None,
    context_processors_func: Callable = None,
    init_app_func: Callable = None,
    process_before_request_func: Callable = None,
    process_after_request_func: Callable = None,
    # babel_func: Callable = None,
    template_filters: Dict[str, Callable] = None,
) -> Flask:
    settings = FlaskSetting()

    # 根据配置来设置app的静态目录和模板
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=settings.template_folder,
        static_folder=settings.static_folder,
        static_url_path="/static",
    )
    container = BackendContainer()
    app.container = container

    robot = load_system_robot()
    app.config["ROBOT"] = robot

    # 匹配有斜杠或无斜杠的规则
    app.url_map.strict_slashes = False
    app.secret_key = settings.secret_key
    app.config["APP_NAME"] = settings.app_name
    # 使用ORJSON来做json序列化
    app.json_encoder = ORJSONEncoder
    app.json_decoder = ORJSONDecoder

    # 允许Cross Origin Resource Sharing
    CORS(app, supports_credentials=True, expose_headers=["Content-Disposition"])

    # 初始化jwt
    jwt_setting = JwtSetting()
    app.config["JWT_SECRET_KEY"] = jwt_setting.secret_key
    app.config["JWT_TOKEN_LOCATION"] = jwt_setting.token_location
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = jwt_setting.access_token_expires
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = jwt_setting.refresh_token_expires
    app.config["JWT_HEADER_NAME"] = jwt_setting.header_name
    app.config["JWT_HEADER_TYPE"] = jwt_setting.header_type

    jwt.init_app(app)

    # 开发环境数据配置
    dev_setting = DevSetting()
    app.config["DEV_SETTING"] = dev_setting

    if blueprint_module:
        blueprint_list = scan_objects_from_module(scan_module=blueprint_module, scan_type=Blueprint)
        for blueprint_item in blueprint_list:
            app.register_blueprint(blueprint_item)

    # 注册异常捕捉处理，该函数以Exception为输入参数
    if error_handler_func:
        app.errorhandler(Exception)(error_handler_func)

    # 初始化上下文进行加载
    if init_app_func:
        with app.app_context():
            init_app_func(app)

    # 注入上下文应用所需要的函数
    if context_processors_func:
        app.context_processor(context_processors_func)

    # 注入请求前预处理的方法
    if process_before_request_func:
        app.before_request(process_before_request_func)

    # 注入请求后处理的方法
    if process_after_request_func:
        app.after_request(process_after_request_func)

    # 注入模板过滤器
    if template_filters:
        for template_name in template_filters:
            app.add_template_filter(template_filters[template_name], template_name)

    # profile
    if settings.profiling:
        app.config["PROFILE"] = True
        # 构建profile_dir
        profile_dir = build_abs_path_by_file(__file__, "../profile")
        Path(profile_dir).mkdir(parents=True, exist_ok=True)
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir=profile_dir)

    return app
