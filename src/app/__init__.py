"""
Creates and configures flask api
"""
import os

from flask import Flask

from .aborter import setup_aborter
from .api import Api
from .auth import setup_auth
from .healthcheck import setup_healthcheck
from .logging import setup_logging
from .resources import actions, site_posts, sites


def setup_api(app: Flask, prefix: str, version: str) -> Api:
    """Set up flask_smorest Api on `app`"""
    full_prefix = f"/{prefix}/{version}"
    spec_config = {
        "API_TITLE": "Example flask REST API",
        "API_VERSION": version,
        "OPENAPI_VERSION": "3.0.2",
        "OPENAPI_URL_PREFIX": f"{full_prefix}/doc",
        "OPENAPI_JSON_PATH": "/documentation.json",
        "OPENAPI_SWAGGER_UI_PATH": "/swagger",
        "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        "OPENAPI_REDOC_PATH": "/redoc",
        "OPENAPI_REDOC_URL": "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
        "OPENAPI_RAPIDOC_PATH": "/rapidoc",
        "OPENAPI_RAPIDOC_URL": "https://unpkg.com/rapidoc/dist/rapidoc-min.js",
    }
    app.config.update(spec_config)
    api = Api(app)
    for bp in [sites.bp, actions.bp, site_posts.bp]:
        api.register_blueprint(bp, url_prefix=full_prefix + bp.url_prefix)

    return api


def create_application() -> Flask:
    """Create, configure and return Flask application"""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    log_file_base_name = os.environ.get("LOG_FILE_BASE_NAME")

    setup_logging(app, log_file_base_name=log_file_base_name)
    api = setup_api(app, "api", "v1")
    setup_aborter(app)  # must be called AFTER setup_api
    setup_auth(app, api)
    setup_healthcheck(app)

    return app
