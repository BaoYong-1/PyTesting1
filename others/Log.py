# encoding=utf-8
import logging.config
import logging

# 读取日志的配置文件
conf_path = 'F:\\PyTesting\\AutoTest\\config\\Logger.conf'
logging.config.fileConfig(conf_path)
# 选择一个日志格式
logger = logging.getLogger('xzs')

def warning(message):
    # 打印warning级别的信息(日志级别较弱，最弱的是debug)
    logger.warning(message)

def debug(message):
    # 打印debug级别的信息（日志信息级别最弱
    logger.debug(message)

def info(message):
    # 打印info级别信息
    logger.info(message)

def error(message):
    # 打印wornging级别信息
    logger.error(message)


def log_test02():
    CONF_LOG = conf_path
    logging.config.fileConfig(CONF_LOG)  # 采用配置文件
    logger1 = logging.getLogger("xzs")
    logger1.debug("Hello xzs")
    logger1 = logging.getLogger()
    logger1.info("Hello root")

if __name__ == '__main__':
    logging.config.fileConfig(conf_path)
    info('info level')
    warning('warning level')
    error('error level')
    debug('debug level')
    log_test02()
