# log
import logging
import time
from functools import wraps

# log
logger = logging.getLogger('Machine Learning Server')

# （可选）开发调试期间选DEBUG，软件成型使用时选INFO
lever_threshold = logging.DEBUG
# lever_threshold = logging.INFO


formatter = logging.Formatter('%(levelname)7s -> %(message)s')
# formatter = logging.Formatter('%(levelname)7s -> %(pathname)s, %(funcName)s, line %(lineno)d,%(message)s') # 仅可用于直接调用logging
logger.setLevel(lever_threshold)

# 窗口调试
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(lever_threshold)
logger.addHandler(console_handler)


# 文件输出调试
# file_handler = logging.FileHandler('Machine Learning Server.log')
# file_handler.setFormatter(formatter)
# file_handler.setLevel(lever_threshold)
# logger.addHandler(file_handler)


def log(entry, level='info'):
    """
    The function `log` logs an entry with a specified level using a logger object.
    
    Args:
      entry: The `entry` parameter is a string that represents the log message that you want to log. It
    can be any text or information that you want to include in the log entry.
      level: The `level` parameter is an optional parameter that specifies the logging level. It has a
    default value of `'info'`. The level is accept by ``util.lever_threshold``, just lever higher than lever_threshold is shown.
    
    Example:
    
    >>> log("name",level='info')
    
    """
    level = level.lower()
    if level not in ['debug', 'info', 'warning', 'error']:
        logger.error('Wrong level input')

    space = '-' * (4 * 0)
    msg = f"{space} {entry}"

    getattr(logger, level)(msg)


def time_this_function(func):
    """simple time decorator.
    
    Example:
    
    >>> @time_this_function
    >>> def add1(x,y):
    ...     time.sleep(1.12)
    ...     return x+y
    >>> add1(1, 0.2)
    1.2
    
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"'{func.__name__}' function used time: {end - start}")
        return result

    return wrapper


def log_this_function(entry="", level='info', log_time=True):
    """
    log time decorator.
    The function logs a given entry with a specified log level and includes the log time if specified.
    
    Args:
      entry: The `entry` parameter is used to specify the message or information that you want to log.
    It is an optional parameter and its default value is an empty string.
      level: The level parameter is used to specify the severity level of the log entry. It can have
    values like 'info', 'warning', 'error', etc. Defaults to info
      log_time: A boolean value indicating whether or not to include the timestamp in the log entry. If
    set to True, the timestamp will be included. If set to False, the timestamp will be omitted.
    
    
    Example:
    
    >>> @log_this_function("name", level="info", log_time=False)
    >>> def add1(x,y):
    ...     time.sleep(1.12)
    ...     return x+y
    >>> add1(1, 0.2)
    1.2
    
    """

    def _time_log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()

            if entry == "":
                entry = "{func.__name__} function"

            if log_time == True:
                log(f"{entry}, time: {end - start}", level)
            else:
                log(entry, level)
            return result

        return wrapper

    return _time_log


if __name__ == "__main__":
    log("name", level='info')


    @time_this_function
    def add(x, y):
        time.sleep(1.12)
        return x + y


    add(1, 0.2)


    @log_this_function("sf", level="debug")
    def add(x, y):
        time.sleep(1.12)
        return x + y


    add(1, 0.2)
