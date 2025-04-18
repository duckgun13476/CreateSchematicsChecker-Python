import time
from functools import wraps
from Checker.lib.log_color import log


##################################################
# 用于测试函数的运行时间v.10
def measure_time(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        log.debug(f"退出时间:{end - start}秒")

    return wrapper


###################################################
# 用于测试函数的运行时间v1.1
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        log.debug(f"函数{func.__name__}执行时间：{end - start}秒")
        return result

    return wrapper


###################################################
# 用于打印函数的名称参数和返回值v1.0

def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.debug(f"名称：{func.__name__}, args:{args},kwargs:{kwargs}")
        result = func(*args, **kwargs)
        log.debug(f"函数{func.__name__} 返回了 ：{result}")
        return result

    return wrapper


###################################################

def error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.debug(f"名称：{func.__name__}, args:{args},kwargs:{kwargs}")
        result = func(*args, **kwargs)
        log.debug(f"函数{func.__name__} 返回了 ：{result}")
        return result

    return wrapper


###################################################
# 用于缓存先前调用的结果以重复使用，用于加速高运算重复调用的情况v1.0
def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            result = func(*args)
            cache[args] = result
            return result

    return wrapper
