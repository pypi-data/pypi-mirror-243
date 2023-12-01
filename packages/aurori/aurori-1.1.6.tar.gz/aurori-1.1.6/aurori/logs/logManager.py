"""
The aurori project

Copyright (C) 2022  Marcus Drobisch,

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__authors__ = ["Marcus Drobisch"]
__contact__ = "aurori@fabba.space"
__credits__ = []
__license__ = "AGPLv3+"

import sys
import collections
import datetime
import threading
import logging
from .logger import Logger

class LogManager(object):
    def __init__(self):
        gettrace = getattr(sys, 'gettrace', None)
        if gettrace and gettrace():
            self.run_in_debug_mode = True
        else:
            self.run_in_debug_mode = False
          
        self.logQueue = collections.deque(maxlen=512)
        self.loggers = {
            "core": Logger("core", self.run_in_debug_mode, app_logger=False)
        }
        self.logger = self.loggers["core"]

        logging.basicConfig(level=logging.INFO, format='[%(asctime)s]-[%(name)s]-[%(levelname)s]: %(message)s', datefmt="%Y-%m-%dT%H:%M:%S")     

    def register_logger(self, logger, name):
        self.loggers[name.lower()] = logger

    def info(self, msg, *args, **kwargs):
        """
        Delegate a info log call to the underlying logger,
        """
        if type(msg) is str:
            try:
                s = msg % args
            except Exception:
                s = msg.format(*args)
            indents = s.replace("\n", "\n" + " " * 29)
            self.logQueue.append(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                " [INFO] : " + indents)
        else:
            s = str(msg)
            indents = s.replace("\n", "\n" + " " * 29)
            self.logQueue.append(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                " [INFO] : " + indents)
        try:
            self.logger.info(msg, *args, **kwargs)
            indents = s.replace("\n", "\n" + " " * 14)
        except Exception as e:
            print("logger failed to print: ", s, e)

    def warning(self, msg, *args, **kwargs):
        """
        Delegate a warning log call to the underlying logger,
        """
        if type(msg) is str:
            try:
                s = msg % args
            except Exception:
                s = msg
            self.logQueue.append(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                " [WARN] : " + s)
        else:
            s = str(msg)
            self.logQueue.append(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                " [WARN] : " + s)

        try:
            self.logger.warning(msg, *args, **kwargs)
        except Exception:
            print("logger failed to print: ", s)

    def error(self, msg, *args, **kwargs):
        """
        Delegate a error log call to the underlying logger,
        """
        if type(msg) is str:
            try:
                s = msg % args
            except Exception:
                s = msg
            self.logQueue.append(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                " [FAIL] : " + s)
        else:
            s = str(msg)
            self.logQueue.append(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                " [FAIL] : " + s)

        try:
            self.logger.error(msg, *args, **kwargs)
        except Exception:
            print("logger failed to print: ", s)

    def debug(self, msg, *args, **kwargs):
        """
        Delegate a error log call to the underlying logger,
        """
        if self.run_in_debug_mode is not True:
            return
        if type(msg) is str:
            try:
                s = msg % args
            except Exception:
                s = msg
            self.logQueue.append(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                " [DEBUG] : " + s)
        else:
            s = str(msg)
            self.logQueue.append(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                " [DEBUG] : " + s)

        try:
            self.logger.debug(msg, *args, **kwargs)
        except Exception:
            print("logger failed to print: ", s)
