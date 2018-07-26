# encoding=utf-8
import logging
import logging.config
from ProjectVar.Var import *
import os

# 读取日志的配置文件
logging.config.fileConfig(project_path + '\\config\\Logger.conf')
# 选择一个日志格式
logger = logging.getLogger('example02')


def warning(message):
    # 打印warning级别的信息(日志级别较弱，最弱的是debug)
    logger.warn(message)


def debug(message):
    # 打印debug级别的信息（日志信息级别最弱
    logger.debug(message)


def info(message):
    # 打印info级别信息
    logger.info(message)


def error(message):
    # 打印wornging级别信息
    logger.error(message)


if __name__ == '__main__':
    a = project_path + '\\config\\Logger.conf'
    print(os.path.exists(a))
    print(a)
    logging.config.fileConfig(project_path + '\\config\\Logger.conf')
    info('info level')
    warning('warning level')
    error('error level')
    debug('debug level')
