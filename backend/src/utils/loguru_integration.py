import logging
from itertools import chain
from types import FrameType
from typing import Any, Union, cast

import uvicorn
from loguru import logger
from uvicorn.supervisors import ChangeReload, Multiprocess


class InterceptHandler(logging.Handler):
    """Logs to loguru from Python logging module"""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        depth = 2
        frame: FrameType = logging.currentframe()

        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger_with_opts = logger.opt(depth=depth, exception=record.exc_info)

        try:
            logger_with_opts.log(level, "{}", record.getMessage())
        except Exception as err:
            safe_msg: Union[Any, str] = getattr(record, "msg", None) or str(record)
            logger_with_opts.warning(
                "Exception logging the following native logger message: {}, {!r}",
                safe_msg,
                err,
            )


def setup_loguru_logging_intercept(level=logging.DEBUG, modules=()) -> None:
    logging.basicConfig(handlers=[InterceptHandler()], level=level)  # noqa
    for logger_name in chain(("",), modules):
        mod_logger = logging.getLogger(logger_name)
        mod_logger.handlers = [InterceptHandler(level=level)]
        mod_logger.propagate = False


def run_uvicorn_loguru(config: uvicorn.Config, force_exit=False) -> None:
    """Same as uvicorn.run but injects loguru logging"""
    server = uvicorn.Server(config=config)
    server.force_exit = force_exit

    setup_loguru_logging_intercept(
        level=logging.getLevelName(config.log_level.upper()),
        modules=("uvicorn.error", "uvicorn.asgi", "uvicorn.access"),
    )

    supervisor_type = None
    if config.should_reload:
        supervisor_type = ChangeReload
    if config.workers > 1:
        supervisor_type = Multiprocess
    if supervisor_type:
        sock = config.bind_socket()
        supervisor = supervisor_type(config, target=server.run, sockets=[sock])
        supervisor.run()
    else:
        server.run()
