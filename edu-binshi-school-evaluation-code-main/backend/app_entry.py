from infra_utility.config_helper import load_to_env
from infra_utility.log_helper import config_logger

from backend import blueprint
from backend.app_config import process_after_request, process_before_request, process_error_handler
from backend.factories import create_flask_app

config_logger(level="INFO", show_file=True, show_thread=True)
load_to_env(__file__, "../app.toml")

flask_app = create_flask_app(
    blueprint_module=blueprint,
    error_handler_func=process_error_handler,
    process_before_request_func=process_before_request,
    process_after_request_func=process_after_request,
)
