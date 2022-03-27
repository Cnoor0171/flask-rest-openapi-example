"""App logging configuration"""
import logging
import logging.config
import math
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import structlog
from flask import Flask, Response, g, has_request_context, request

LOGGER = structlog.stdlib.get_logger(__name__)


def log_request() -> None:
    """Starts performance counter and logs incomming requests"""
    g.req_start_time_s = time.perf_counter()  # pylint: disable=assigning-non-slot
    path = request.url_rule.rule if request.url_rule else request.path
    LOGGER.info(
        "Recieved request",
        method=request.method,
        path=path,
        path_params=request.view_args,
        q_params=request.query_string.decode(),
    )


def log_response(response: Response) -> Response:
    """Ends performance counter and logs outgoing response with request duration"""
    req_end_time_s = time.perf_counter()
    dur_ms = (req_end_time_s - g.req_start_time_s) * 1000
    LOGGER.info(
        "Sending response", code=response.status_code, duration=f"{dur_ms:.2f}ms"
    )
    return response


def setup_logging(
    app: Flask, log_to_term: bool = True, log_file_base_name: str | None = None
) -> None:
    """Sets up app logging configuration"""

    def request_id_adder(
        _logger: Any, _name: str, event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        if has_request_context():
            if not getattr(g, "request_id", None):
                g.request_id = str(uuid4())  # pylint: disable=assigning-non-slot
            event_dict["request_id"] = g.request_id
        return event_dict

    def pathname_lineno_combiner(
        _logger: Any, _name: str, event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        pathname = event_dict.pop("pathname")
        lineno = event_dict.pop("lineno")
        event_dict["line"] = f" {pathname}:{lineno}"
        return event_dict

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            request_id_adder,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.CallsiteParameterAdder(
                [
                    structlog.processors.CallsiteParameter.PATHNAME,
                    structlog.processors.CallsiteParameter.LINENO,
                ]
            ),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    handlers: dict[str, dict[str, Any]] = {}
    if log_to_term:
        handlers["terminal"] = {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "console",
        }
    if log_file_base_name:
        time_stamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        log_file = Path(log_file_base_name).with_suffix(f".{time_stamp}.jsonl")
        log_file.parent.mkdir(exist_ok=True, parents=True)
        handlers["file"] = {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_file,
            "formatter": "json",
            "backupCount": math.inf,
            "maxBytes": 1 * 1000 * 1000,
        }
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "json": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        structlog.processors.TimeStamper(fmt="iso"),
                        structlog.processors.format_exc_info,
                        structlog.processors.JSONRenderer(),
                    ],
                },
                "console": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        pathname_lineno_combiner,
                        structlog.dev.ConsoleRenderer(colors=True, sort_keys=False),
                    ],
                },
            },
            "handlers": handlers,
            "loggers": {
                "": {
                    "handlers": list(handlers.keys()),
                    "level": "DEBUG",
                    "propagate": True,
                },
            },
        }
    )
    logging.getLogger("werkzeug").disabled = True

    app.before_request(log_request)
    app.after_request(log_response)
