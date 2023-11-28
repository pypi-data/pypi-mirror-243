"""
Provides a convenient Decorator Function for Debugging!
"""

# region	|=-=-=-=|Import  Section|=-=-=-=|
import functools
import datetime as dt
import logging as log
import os
opj = os.path.join
# endregion
# 			|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|

# region	|=-=-=-=|Setup Section|=-=-=-=|
__LOGGER__ = r'log.log'
# endregion
# 			|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|


def debugging(export_dir: str = None, console: bool = True):
    if not console:
        if export_dir is None:
            log_mode = log.FileHandler(__LOGGER__)
        else:
            log_mode = log.FileHandler(opj(export_dir, __LOGGER__))
    else:
        log_mode = log.StreamHandler()

    dbgLog = log.getLogger('debugging')
    dbgLog.setLevel(log.INFO)
    dbgLog_handler = log_mode
    formatter = log.Formatter(
        '%(asctime)s [%(levelname)s]: Decorator => %(name)s >>> %(message)s'
    )
    dbgLog_handler.setFormatter(formatter)
    dbgLog.addHandler(dbgLog_handler)

    def decorator(func):
        func_name = func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                dbgLog.info(
                    f"[Success Log]: function => \
{{{func_name}(*args{args}, **kwargs{kwargs})}}: \
returned -> {result}"
                )
            except Exception as e:
                dbgLog.error(
                    f"[Error Log]: function => \
{{{func_name}(*args{args}, **kwargs{kwargs})}}: {str(e)}"
                )
                result = None

            return result

        return wrapper

    return decorator


def process_time(func):
    ptLog = log.getLogger('process_time')
    ptLog.setLevel(log.INFO)
    ptLog_handler = log.StreamHandler()
    formatter = log.Formatter(
        '%(asctime)s [%(levelname)s]: Decorator => %(name)s >>> %(message)s'
    )
    ptLog_handler.setFormatter(formatter)
    ptLog.addHandler(ptLog_handler)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = dt.datetime.now()
        result = func(*args, **kwargs)
        ptLog.info(f"[ProcessTime Info]: function => \
{{{func.__name__}(*args{args}, **kwargs{kwargs})}} -> \
{(dt.datetime.now() - start).total_seconds()}s")

        return result

    return wrapper


if __name__ == '__main__':
    logfile = r"E:\DevelopmentEnvironment\ERROR LOG"

    @process_time
    @debugging(logfile, False)
    def test(a, b):
        return a / b

    print(test(9, 4))
