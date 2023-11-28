from memodules.alphabet_to_integer import *
from memodules.error_lib import *
from dataclasses import dataclass
import re

class OVER_RANGE(Exception):
    """Max Range of Excel Application:\nMaxRows = 1048576, MaxColumn = 16384\n
    When it exceeds that number, an 'OVER_RANGE' error occurs"""
    def __init__(self, mode: str):
        self.mode = mode
    
    def __str__(self) -> str:
        return f'{self.mode} Range Over'
    
def isoverrange(target: int, mode: str, ifmode: bool=False) -> bool:
    """mode = 'r': target > 1048576 -> OVER_RANGE Error\n
    mode = 'c': target > 16384 -> OVER_RANGE Error"""
    if mode.lower().startswith('r'):
        if target > xl_Data_Dict._MAX_ROW:
            if ifmode:
                return True
            else:
                raise OVER_RANGE(mode='Rows')
    elif mode.lower().startswith('c'):
        if target > xl_Data_Dict._MAX_COLUMN:
            if ifmode:
                return True
            else:
                raise OVER_RANGE(mode='Columns')
    else:
        modeselectionerror()

@dataclass(frozen=True)
class xl_Data_Dict:
    """xl_Data_Dict.varlist()で定数リスト取得可"""
    _MAX_ROW: int = 1048576
    """The Bottom Value of an Excel Application Worksheet"""
    _MAX_COLUMN: int = 16384
    """The Rightmost Value of an Excel Application Worksheet"""
    _MAX_COLUMN_LETTER: str = frozenset('XFD')
    """The Rightmost Index Letter an Excel Application Worksheet"""
    
    @classmethod
    def varlist(cls):
        initialized_variables = []
        for name, value in cls.__dict__.items():
            if not name.startswith("__") and not callable(value):
                if value == getattr(cls, name):
                    initialized_variables.append(name)
        return initialized_variables

def cell_index_increment(target: str, incrementvalue: int=1, mode: str='r'):
    """target = 'C7'\n
    mode = 'r': -> 'C8'\n
    mode = 'c': -> 'D7'"""
    cidx, ridx = SIsplit(target)
    result = ''
    if mode.lower().startswith('r'):
        ridx = int(ridx) + incrementvalue
        result = f'{cidx}{ridx}'
    elif mode.lower().startswith('c'):
        cidx = ItA(AtI(cidx) + incrementvalue, True)
        result = f'{cidx}{ridx}'
        
    return result
                
def range_index_exchange(target, mode: str):
    """mode = 'range': 'C7' ->tuple (7, 3)(int, int)\n
    mode = 'cells': [7, 3] or (7, 3) ->str 'C7'"""
    #mode分岐
    row = ''
    column = ''
    if mode == 'range':
        column, row = SIsplit(target)
        column = AtI(column)
        return (int(row), column)
    elif mode == 'cell':
        row, column = target
        column = ItA(column, True)
        return f'{column}{row}'
    else:
        modeselectionerror()
        
if __name__ == '__main__':
    print(xl_Data_Dict)