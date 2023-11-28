import os
import logging
import datetime as dt
from typing import NewType
from dataclasses import dataclass

__all__ = [
    'Log_Out',
    'LEVEL',
    'MODE',
]

# |=-=-=-=|Setup Section|=-=-=-=|
# alias
op = os.path

# type
level = NewType('level', int)
mode = NewType('mode', str)

# initialize valiable
_PARENT_MODULE = op.basename(op.abspath(__file__))
_PARENT_NAME = op.splitext(_PARENT_MODULE)[0]
_DEFAULT_PATH = r'E:\DevelopmentEnvironment\python\logs'
_DEFAULT_LOGNAME = (
    f'{_PARENT_MODULE}[{dt.datetime.now():%Y%m%d%H%M%S}].log'
)
_ERROR_LOG_DIR = r'E:\DevelopmentEnvironment\ERROR LOG\EXCEPTION.log'
_ERROR_HANDLE = logging.FileHandler(_ERROR_LOG_DIR)
# |=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|


@dataclass
class LEVEL:
    """This Dataclass Defines The Custom Logging Level"""
    N: level = logging.NOTSET
    """Logging Level 'NOTSET'"""
    D: level = logging.DEBUG
    """Logging Level 'DEBUG'"""
    I: level = logging.INFO
    """Logging Level 'INFO'"""
    W: level = logging.WARNING
    """Logging Level 'WARNING'"""
    E: level = logging.ERROR
    """Logging Level 'ERROR'"""
    C: level = logging.CRITICAL
    """Logging Level 'CRITICAL'"""


@dataclass(frozen=True)
class MODE:
    """This Dataclass Defines The Handle Mode"""
    F: mode = frozenset('file')
    """Logging Output to File"""
    S: mode = frozenset('stream')
    """Logging Output to Console"""


class Log_Out:
    def __init__(
        self,
        output_dir_path: str = None,
        output_logname: str = None,
        handle_mode: MODE = MODE.F
    ):
        """handle_mode('file' or not set) = log data is input to file\n
        'stream' = log data is output to console"""
        if output_dir_path is None:
            output_dir_path = _DEFAULT_PATH
        if output_logname is None:
            output_logname = _DEFAULT_LOGNAME
        self._DIRECTORY: str = op.join(output_dir_path, output_logname)

        if handle_mode is MODE.F:
            self._HANDLEMODE = logging.FileHandler(self._DIRECTORY)
        elif handle_mode is MODE.S:
            self._HANDLEMODE = logging.StreamHandler()

    def __enter__(self):
        # create a logger preset
        self.normal_debug_logger = (
            logging.getLogger(f'normal_debug_log[{_PARENT_NAME}]')
        )
        self.normal_debug_logger.setLevel(logging.DEBUG)
        self.valiable_debug_logger = (
            logging.getLogger(f'look_valiable_content[{_PARENT_NAME}]')
        )
        self.valiable_debug_logger.setLevel(logging.DEBUG)

        # |=-=-=-=|Special Logger|=-=-=-=|
        logformat = logging.Formatter(
            fmt=(
                '''%(asctime)s: %(name)s [ %(lineno)d ] \
                {\n\t%(message)s\n}\n'''
            ),
            datefmt='%y%m%d%H%M%S'
        )
        self.exception_endpattern = (
            logging.getLogger('!!!EXCEPTION LOG!!!')
        )
        self.exception_endpattern.setLevel(logging.ERROR)
        _ERROR_HANDLE.setFormatter(logformat)
        self.exception_endpattern.addHandler(_ERROR_HANDLE)
        # |=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|
        return self

    def val(
        self,
        log_out_content: str,
        custom_loglevel: LEVEL = None
    ) -> None:
        """\
            The custom_loglevel should be
             set using the class 'LEVEL' variable
        """
        if custom_loglevel is not None:
            self.valiable_debug_logger.setLevel(custom_loglevel)

        logformat = logging.Formatter(
            fmt=(
                '''%(asctime)s: %(levelname)s - %(name)s {\t%(message)s\t}'''
            ),
            datefmt='%y%m%d%H%M%S'
        )
        self._HANDLEMODE.setFormatter(logformat)
        self.valiable_debug_logger.addHandler(self._HANDLEMODE)

        self.valiable_debug_logger.debug(f'value: {log_out_content}')

    def flog(
        self,
        custom_loglevel: LEVEL = None,
        **kwargs,
    ) -> None:
        """The custom_loglevel should be \
        set using the class 'LEVEL' variable"""
        if custom_loglevel is not None:
            self.valiable_debug_logger.setLevel(custom_loglevel)

        logcontent = ''
        for key, value in kwargs.items():
            logcontent += f'\t{key}: {value}\n'

        logformat = logging.Formatter(
            fmt=(
                '''%(asctime)s: %(levelname)s - %(name)s {\n%(message)s}'''
            ),
            datefmt='%y%m%d%H%M%S'
        )
        self._HANDLEMODE.setFormatter(logformat)
        self.valiable_debug_logger.addHandler(self._HANDLEMODE)

        self.valiable_debug_logger.debug(logcontent)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if any(val is not None for val in [exc_type, exc_val, exc_tb]):
            logging.error(
                msg='Exception Exit Log: ',
                exc_info=True,
            )
        self._HANDLEMODE.close()
        _ERROR_HANDLE.close()


if __name__ == '__main__':
    with Log_Out(
        r"E:\DevelopmentEnvironment\python\logs",
        'log_module_sample.log',
    ) as log:
        a = 0
        b = 'val:b'
        c = __name__
        log.flog(a=a, b=b, c=c)
        a = 1 + 2 + 3 + 4 + 5 * 0
        b = 'val:after b'
        log.flog(a=a, b=b, c=c)
