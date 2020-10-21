# coding=utf-8
__all__ = ['getLogger']

import logging
import logging.config
import os
from datetime import date
_BASE_DIR = os.getcwd()
DIR_DEBUG = os.path.join(_BASE_DIR, 'logs', 'debug')
DIR_INFO = os.path.join(_BASE_DIR, 'logs', 'info')
DIR_ERROR = os.path.join(_BASE_DIR, 'logs', 'error')

if not os.path.exists(DIR_DEBUG):
    os.makedirs(DIR_DEBUG)
if not os.path.exists(DIR_INFO):
    os.makedirs(DIR_INFO)
if not os.path.exists(DIR_ERROR):
    os.makedirs(DIR_ERROR)

IS_INIT = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # 日志输出格式设置
    "formatters": {
        "simple": {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },

    "handlers": {
        # 控制台处理器,控制台输出
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        # 默认处理器, 文件大小滚动
        "debug": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            'filename': os.path.join(DIR_DEBUG, '{}debug.log'.format(date.today())),
            "maxBytes": 1024 * 1024 * 16,  # 16 MB
            "backupCount": 64,
            "encoding": "utf8"
        },
        # 错误日志, 文件大小滚动
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(DIR_ERROR, '{}error.log'.format(date.today())),
            'maxBytes': 1024 * 1024 * 2,
            'backupCount': 10,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # info 及以上级别, 日期滚动
        'info': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            "formatter": "simple",
            'filename': os.path.join(DIR_INFO, '{}info.log'.format(date.today())),
            'when': 'D',  # 单位： 天
            'interval': 1,  # 滚动周期
            'backupCount': 30,  # 备份30天
            "encoding": "utf8"
        },
    },
    'loggers': {
        'websockets': {
            'handlers': ['debug', 'console'],
            'level': "ERROR",
            'propagate': False
        },
        'asyncio': {
            'handlers': ['debug', 'console'],
            'level': "ERROR",
            'propagate': False
        },
        'comtypes': {
            'handlers': ['debug', 'console'],
            'level': "INFO",
            'propagate': False
        },
    },
    "root": {
        'handlers': ['debug', 'error', 'info', 'console'],
        'level': "DEBUG",
        'propagate': False
    }
}


def initLogConf():
    """
    配置日志
    """
    global IS_INIT
    if IS_INIT:
        return
    logging.config.dictConfig(LOGGING)
    logging.debug("Init logging")
    IS_INIT = True


def getLogger(name):
    return logging.getLogger(name)


initLogConf()

if __name__ == '__main__':
    logger = getLogger('aaa')
    logger.debug('debug')
    logger.info('info')
    logger.error('error')
