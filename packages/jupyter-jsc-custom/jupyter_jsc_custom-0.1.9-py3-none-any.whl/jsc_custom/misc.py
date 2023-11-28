import copy
import json
import logging
import os
import socket
import sys

import yaml
from jsonformatter import JsonFormatter
from jupyterhub.app import app_log

logged_logger_name = os.environ.get("LOGGER_NAME", "JupyterHub")
logger_name = "JupyterHub"

_custom_config_cache = {}
_custom_config_last_update = 0
_custom_config_file = os.environ.get("CUSTOM_CONFIG_PATH")

_logging_cache = {}


def get_logging_config():
    global _logging_cache
    return _logging_cache


def get_custom_config():
    global _custom_config_cache
    global _custom_config_last_update
    global _logging_cache

    # Only update custom_config, if it has changed on disk
    try:
        last_change = os.path.getmtime(_custom_config_file)
        if last_change > _custom_config_last_update:
            app_log.debug("Load custom config file.")
            with open(_custom_config_file, "r") as f:
                ret = yaml.full_load(f)
            _custom_config_last_update = last_change
            _custom_config_cache = ret

            if _custom_config_cache.get("logging", {}) != _logging_cache:
                _logging_cache = _custom_config_cache.get("logging", {})
                app_log.debug("Update Logger")
                update_extra_handlers()

    except:
        app_log.exception("Could not load custom config file")
    else:
        return _custom_config_cache


_reservations_cache = {}
_reservations_last_update = 0
_reservations_file = os.environ.get("RESERVATIONS_FILE")


def get_reservations():
    global _reservations_cache
    global _reservations_last_update
    try:
        # Only update reservations, if it has changed on disk
        last_change = os.path.getmtime(_reservations_file)
        if last_change > _reservations_last_update:
            app_log.debug("Load reservation file")
            with open(_reservations_file, "r") as f:
                ret = json.load(f)
            _reservations_last_update = last_change
            _reservations_cache = ret
    except:
        app_log.exception("Could not load reservation file")
    finally:
        return _reservations_cache


_incidents_cache = {}
_incidents_last_update = 0
_incidents_file = os.environ.get("INCIDENTS_FILE")


def get_incidents():
    global _incidents_cache
    global _incidents_last_update
    try:
        last_change = os.path.getmtime(_incidents_file)
        if last_change > _incidents_last_update:
            app_log.debug("Load incidents file")
            with open(_incidents_file, "r") as f:
                ret = json.load(f)
            _incidents_last_update = last_change
            _incidents_cache = ret
    except:
        app_log.exception("Could not load incidents file")
    return _incidents_cache


async def create_ns(user):
    ns = dict(user=user)
    if user:
        auth_state = await user.get_auth_state()
        if "refresh_token" in auth_state.keys():
            del auth_state["refresh_token"]
        ns["auth_state"] = auth_state
    return ns


class ExtraFormatter(logging.Formatter):
    dummy = logging.LogRecord(None, None, None, None, None, None, None)
    ignored_extras = [
        "args",
        "asctime",
        "created",
        "exc_info",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName",
    ]

    def format(self, record):
        extra_txt = ""
        for k, v in record.__dict__.items():
            if k not in self.dummy.__dict__ and k not in self.ignored_extras:
                extra_txt += " --- {}={}".format(k, v)
        message = super().format(record)
        return message + extra_txt


# Translate level to int
def get_level(level_str):
    if type(level_str) == int:
        return level_str
    elif level_str.upper() in logging._nameToLevel.keys():
        return logging._nameToLevel[level_str.upper()]
    elif level_str.upper() == "TRACE":
        return 5
    elif level_str.upper().startswith("DEACTIVATE"):
        return 99
    else:
        try:
            return int(level_str)
        except ValueError:
            pass
    raise NotImplementedError(f"{level_str} as level not supported.")


# supported classes
supported_handler_classes = {
    "stream": logging.StreamHandler,
    "file": logging.handlers.TimedRotatingFileHandler,
    "smtp": logging.handlers.SMTPHandler,
    "syslog": logging.handlers.SysLogHandler,
}

# supported formatters and their arguments
supported_formatter_classes = {"json": JsonFormatter, "simple": ExtraFormatter}
json_fmt = {
    "asctime": "asctime",
    "levelno": "levelno",
    "levelname": "levelname",
    "logger": logged_logger_name,
    "file": "pathname",
    "line": "lineno",
    "function": "funcName",
    "Message": "message",
}
simple_fmt = f"%(asctime)s logger={logged_logger_name} levelno=%(levelno)s levelname=%(levelname)s file=%(pathname)s line=%(lineno)d function=%(funcName)s : %(message)s"
supported_formatter_kwargs = {
    "json": {"fmt": json_fmt, "mix_extra": True},
    "simple": {"fmt": simple_fmt},
}


def update_extra_handlers():
    global _logging_cache
    logging_config = copy.deepcopy(_logging_cache)
    logger = logging.getLogger(logger_name)

    if logging.getLevelName(5) != "TRACE":
        # First call
        # Remove default StreamHandler
        if len(logger.handlers) > 0:
            logger.removeHandler(logger.handlers[0])

        # In trace will be sensitive information like tokens
        logging.addLevelName(5, "TRACE")

        def trace_func(self, message, *args, **kws):
            if self.isEnabledFor(5):
                # Yes, logger takes its '*args' as 'args'.
                self._log(5, message, args, **kws)

        logging.Logger.trace = trace_func
        logger.setLevel(5)

    logger_handlers = logger.handlers
    handler_names = [x.name for x in logger_handlers]

    for handler_name, handler_config in logging_config.items():
        if (not handler_config.get("enabled", False)) and handler_name in handler_names:
            # Handler was disabled, remove it
            logger.handlers = [x for x in logger_handlers if x.name != handler_name]
            logger.debug(f"Logging handler removed ({handler_name})")
        elif handler_config.get("enabled", False):
            # Recreate handlers which has changed their config
            configuration = copy.deepcopy(handler_config)

            # map some special values
            if handler_name == "stream":
                if configuration["stream"] == "ext://sys.stdout":
                    configuration["stream"] = sys.stdout
                elif configuration["stream"] == "ext://sys.stderr":
                    configuration["stream"] = sys.stderr
            elif handler_name == "syslog":
                if configuration["socktype"] == "ext://socket.SOCK_STREAM":
                    configuration["socktype"] = socket.SOCK_STREAM
                elif configuration["socktype"] == "ext://socket.SOCK_DGRAM":
                    configuration["socktype"] = socket.SOCK_DGRAM

            _ = configuration.pop("enabled")
            formatter_name = configuration.pop("formatter")
            level = get_level(configuration.pop("level"))
            none_keys = []
            for key, value in configuration.items():
                if value is None:
                    none_keys.append(key)
            for x in none_keys:
                _ = configuration.pop(x)

            # Create handler, formatter, and add it
            handler = supported_handler_classes[handler_name](**configuration)
            formatter = supported_formatter_classes[formatter_name](
                **supported_formatter_kwargs[formatter_name]
            )
            handler.name = handler_name
            handler.setLevel(level)
            handler.setFormatter(formatter)
            if handler_name in handler_names:
                # Remove previously added handler
                logger.handlers = [x for x in logger_handlers if x.name != handler_name]
            logger.addHandler(handler)

            if "filename" in configuration:
                # filename is already used in log.x(extra)
                configuration["file_name"] = configuration["filename"]
                del configuration["filename"]
            logger.debug(f"Logging handler added ({handler_name})", extra=configuration)
