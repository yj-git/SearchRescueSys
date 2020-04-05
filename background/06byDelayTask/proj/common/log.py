import logging
from logging.handlers import TimedRotatingFileHandler

LOG_ROOT_PATH = r'task_log.txt'


def init_logger():
    '''
        初始化 logger 并配置相关设置
        注意 logger 不会叠加，在多个地方创建logger只会执行一个
    @return:
    '''
    # 大概的思路:
    # 1 创建 logging
    logger = logging.getLogger('delay_task_log')
    # 2 设置监听 level
    logger.setLevel(logging.INFO)
    # TODO:[*] 20-04-05 此处若使用 按时间切分 如何确定最终的 path -> file_name
    # 3 创建 handler
    # 3-1 将日志消息发送到磁盘文件，并支持日志文件按时间切割
    # err:IsADirectoryError: [Errno 21] Is a directory:
    file_handler = TimedRotatingFileHandler(LOG_ROOT_PATH)
    # 3-2 设置日志记录的 format
    log_format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_format = logging.Formatter(log_format_str)
    file_handler.setFormatter(log_format)
    # 4 对创建的logger 添加 handler
    logger.addHandler(file_handler)
    return logger

logger=init_logger()



