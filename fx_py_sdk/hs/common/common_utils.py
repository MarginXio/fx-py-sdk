# -*- coding: utf-8 -*-
import os
import time
import logging
from threading import RLock
from datetime import datetime

def get_info_logger(name, filename: str=None):
    handler = logging.StreamHandler() if filename is None else logging.FileHandler(filename=filename)
    return get_logger(name, level=logging.INFO, handler=handler)

def get_debug_logger(name, filename: str=None):
    handler = logging.StreamHandler() if filename is None else logging.FileHandler(filename=filename)
    return get_logger(name, level=logging.DEBUG, handler=handler)

def get_warn_logger(name, filename: str=None):
    handler = logging.StreamHandler() if filename is None else logging.FileHandler(filename=filename)
    return get_logger(name, level=logging.WARN, handler=handler)

def get_error_logger(name, filename: str=None):
    handler = logging.StreamHandler() if filename is None else logging.FileHandler(filename=filename)
    return get_logger(name, level=logging.ERROR, handler=handler)

def get_logger(name, level=logging.INFO, handler=logging.StreamHandler()):
    LOG_FORMAT = "%(asctime)s.%(msecs)03d - %(levelname)s - [%(processName)s|%(threadName)s] - [%(filename)s - %(funcName)s] - line %(lineno)s: %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    logger = logging.getLogger(name)  # __name__
    logger.setLevel(level=level)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# define logger
logger = get_logger(__name__)

g_request_id = int(time.time() % 10000)
g_request_id_lock = RLock()
def get_and_incr_request_id():
    global g_request_id
    with g_request_id_lock:
        g_request_id += 1
        # 4294967295是2的32次方-1
        if g_request_id >= 4294967295:
            g_request_id = int(time.time() % 10000)
        ret_id = g_request_id
    return ret_id


g_conn_id = 0
g_conn_id_lock = RLock()
def init_conn_id(conn_id):
    global g_conn_id
    with g_conn_id_lock:
        g_conn_id = conn_id
    return g_conn_id
def get_and_incr_conn_id():
    global g_conn_id
    with g_conn_id_lock:
        g_conn_id += 1
        # 4294967295是2的32次方-1
        if g_conn_id >= 4294967295:
            g_conn_id = 0
        ret_id = g_conn_id
    return ret_id


def Singleton(cls):
    """创建单实例"""
    def _singleton(*args, **kargs):
        if not hasattr(cls, 'instance'):
            cls.instance = cls(*args, **kargs)
        return cls.instance
    return _singleton


def now_to_int():
    # 转换成时间秒, 用time.time()可以返回有小数点如0.1的秒整数
    return int(time.mktime(datetime.now().timetuple()))


def now_to_str(format="%Y%m%d"):
    """
    e.g. DateUtils.to_str(DateUtils.now(), format="%Y-%m-%d %H:%M:%S.%f")[:-3] = "2019-01-22 00:49:25.216"
    :param format: "%Y%m%d%H%M%S.%f" 格式为 "年月日时分秒.6位毫秒" 经[:-3]可以变为3位毫秒
    :return:
    """
    return datetime.now().strftime(format)  # 转成字面整型字符串, e.g. date: 2009-12-08 16:34:00 -> '20091208163400'


def grim_reaper(signum, frame):
    """
    import signal
    signal.signal(signal.SIGCHLD, grim_reaper)
    """
    while True:
        try:
            pid, status = os.waitpid(
                -1,          # Wait for any child process
                 os.WNOHANG  # Do not block and return EWOULDBLOCK error
            )
        except OSError:
            return
        if pid == 0:  # no more zombies
            return
