#   Copyright 2019 AUI, Inc. Washington DC, USA
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import sys
import inspect
import logging

import skriba.messenger
from datetime import datetime

CALLER_FUNCTION = 1


class LoggingFormatter(logging.Formatter):
    start_msg = "[ {time} ] ".format(time=skriba.messenger.SystemMessage.magenta_dim("%(asctime)s"))
    middle_msg = "{level}".format(level="%(levelname)8s")
    execution_msg = " {name} [ {filename} ]: {exec_info}: ".format(
        name="%(name)10s",
        filename="%(filename)-20s",
        exec_info=skriba.messenger.SystemMessage.blue_dim("%(callchain)%(lineno)-45s"))

    message = "%(message)s"

    FORMATS = {
        logging.DEBUG: start_msg + skriba.messenger.SystemMessage.green(middle_msg) + execution_msg + message,
        logging.INFO: start_msg + skriba.messenger.SystemMessage.blue(middle_msg) + execution_msg + message,
        logging.WARNING: start_msg + skriba.messenger.SystemMessage.yellow(middle_msg) + execution_msg + message,
        logging.ERROR: start_msg + skriba.messenger.SystemMessage.red(middle_msg) + execution_msg + message,
        logging.CRITICAL: start_msg + skriba.messenger.SystemMessage.red_highlight(middle_msg) + execution_msg + message
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(logger_name=None):
    from dask.distributed import get_worker

    function = inspect.stack()[CALLER_FUNCTION].function
    module_path = inspect.stack()[CALLER_FUNCTION].filename
    module = os.path.basename(module_path).strip(".py")
    #lineno = inspect.stack()[CALLER_FUNCTION].lineno

    extra = {'callchain': f"{module}.{function}"}

    if logger_name is None:
        logger_name = "LOGGER"

    try:
        worker = get_worker()

    except ValueError:
        # Scheduler processes
        logger_dict = logging.Logger.manager.loggerDict
        if logger_name in logger_dict:
            logger = logging.getLogger(logger_name)
        else:
            # If main logger is not started using client function it defaults to printing to term.
            logger = logging.getLogger(logger_name)
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(LoggingFormatter())
            logger.addHandler(handler)
            logger.setLevel(logging.getLevelName('INFO'))

        logger = logging.LoggerAdapter(logger, extra)
        return logger

    try:
        logger = worker.plugins['worker_logger'].logger
        logger = logging.LoggerAdapter(logger, extra)
        return logger

    except Exception as error:
        print("Could not load worker logger: {}".format(error))
        print(worker.plugins.keys())

        return logging.getLogger()


def setup_logger(
        logger_name=None,
        log_to_term=False,
        log_to_file=True,
        log_file='LOGGER',
        log_level='INFO',
):
    """To set up as many loggers as you want"""
    if logger_name is None:
        logger_name = "LOGGER"

    function = inspect.stack()[CALLER_FUNCTION].function
    module_path = inspect.stack()[CALLER_FUNCTION].filename
    module = os.path.basename(module_path).strip(".py")
    lineno = inspect.stack()[CALLER_FUNCTION].lineno

    extra = {'callchain': f"{module}.{function}:{lineno}"}

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.getLevelName(log_level))

    logger.handlers.clear()

    if log_to_term:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(LoggingFormatter())
        logger.addHandler(handler)

    if log_to_file:
        log_file = log_file + datetime.today().strftime('%Y%m%d_%H%M%S') + '.log'
        handler = logging.FileHandler(log_file)
        handler.setFormatter(LoggingFormatter())
        logger.addHandler(handler)

    logger = logging.LoggerAdapter(logger, extra)
    return logger


def get_worker_logger_name(logger_name=None):
    from dask.distributed import get_worker
    if logger_name is None:
        logger_name = "LOGGER"

    return logger_name + '_' + str(get_worker().id)


def setup_worker_logger(
        logger_name,
        log_to_term,
        log_to_file,
        log_file,
        log_level,
        worker_id
):
    parallel_logger_name = logger_name + '_' + str(worker_id)

    function = inspect.stack()[CALLER_FUNCTION].function
    module_path = inspect.stack()[CALLER_FUNCTION].filename
    module = os.path.basename(module_path).strip(".py")
    lineno = inspect.stack()[CALLER_FUNCTION].lineno

    extra = {'callchain': f"{module}.{function}:{lineno}"}

    logger = logging.getLogger(parallel_logger_name)
    logger.setLevel(logging.getLevelName(log_level))

    if log_to_term:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(LoggingFormatter())
        logger.addHandler(handler)

    if log_to_file:
        log_file = log_file + '_' + str(worker_id) + '_' + datetime.today().strftime('%Y%m%d_%H%M%S') + '.log'
        handler = logging.FileHandler(log_file)
        handler.setFormatter(LoggingFormatter())
        logger.addHandler(handler)

    logger = logging.LoggerAdapter(logger, extra)
    return logger
