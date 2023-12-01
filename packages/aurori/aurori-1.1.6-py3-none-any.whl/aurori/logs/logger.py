import sys
import threading
import collections
import datetime
import logging


class Logger(object):
    def __init__(self, name, run_in_debug_mode= False, app_logger=True):
        self.run_in_debug_mode = run_in_debug_mode
        if app_logger:
            name = "APP." + ".".join(name.split(".")[1:])         
        self.logger = logging.getLogger(f'{name.upper()}')
        self.logQueue = collections.deque(maxlen=512)

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
            self.logger.info(msg)
            indents = s.replace("\n", "\n" + " " * 14)
        except Exception as e:
            print("logger failed to print: ", s, e)

    def warning(self, msg, *args):
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
            self.logger.warn(msg)
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
            self.logger.error(msg)
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
            self.logger.debug(msg)
        except Exception:
            print("logger failed to print: ", s)

