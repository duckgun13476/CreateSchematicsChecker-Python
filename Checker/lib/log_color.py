import colorlog
import logging
from Checker.config import log_path

console_handler = logging.StreamHandler()

console_handler.setLevel(logging.DEBUG)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white'
    },
    secondary_log_colors={},
    style='%'
)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(log_path, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)  # 设置文件处理器的日志级别
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))  # 设置文件格式
log = colorlog.getLogger()

if not log.handlers:
    log.setLevel(logging.DEBUG)
    log.addHandler(console_handler)
    log.addHandler(file_handler)  # 添加文件处理器

if __name__ == "__main__":
    # 测试不同级别的日志
    log.debug("这是一条 DEBUG 级别的日志")
    log.info("这是一条 INFO 级别的日志")
    log.warning("这是一条 WARNING 级别的日志")
    log.error("这是一条 ERROR 级别的日志")
    log.critical("这是一条 CRITICAL 级别的日志")

