import re

def AtI(alphabet: str) -> int:
    """A(or a) -> 1\n
    AA(or aa) -> 27"""
    result = 0
    if type(alphabet) == list:
        result = []
        for i in alphabet:
            mid = 0
            girder = len(i) - 1
            for n in i:
                mid += (ord(n.upper()) - ord('A') + 1) * (26 ** girder)
                girder -= 1
            
            result.append(mid)
    elif type(alphabet) == str:
        girder = len(alphabet) - 1
        for i in alphabet:
            result += (ord(i.upper()) - ord('A') + 1) * (26 ** girder)
            girder -= 1
        
    return result

def ItA(integer: int, large: bool=False) -> str:
    """integer = 1, large = False -> a\n
    integer = 27, large = True -> AA"""
    result = ''
    tgt = integer
    find = False
    g = 0
    mid = 0
    girder = 0
    while find == False:
        if g == 0:
            if integer <= 1:
                find = True
                girder = 1
        else:
            for i in range(0, g+1):
                mid += (26 ** i)
            if integer < mid:
                find = True
                girder = g
            else:
                mid = 0
                
        g += 1
        
    alp = []
    for gi in range(girder-1, -1, -1):
        for i in range(1, 27):
            if tgt < (26 ** gi) * (i + 1):
                alp.append(i)
                tgt -= (26 ** gi) * i
                break
            elif i == 26:
                alp.append(26)
                tgt -= (26 ** gi) * 26
            
    for i in alp:
        result += chr(i + ord('A') - 1)
    
    return result.lower() if large == False else result.upper()

def pickalpha(target):
    """example: 
    pickalpha('A1') -> 'A'
    pickalpha(['A1', 'AT1']) -> ['A', 'AT']"""
    result = ''
    if type(target) == list:
        result = [''] * len(target)
        i = 0
        for s in target:
            for ss in s:
                if ss.isalpha():
                    result[i] += ss
                    
            i += 1
    elif type(target) == str:
        for s in target:
            if s.isalpha():
                result += s
                
    return result

def SIsplit(target: str) -> list[str, str]:
    result = ['', '']
    for s in target:
        if s.isalpha():
            result[0] += s
        else:
            result[1] += s
            
    return result

def alphain(string):
    pattern = r'[A-Za-z]+'
    match = re.search(pattern, string)
    return match is not None
    
if __name__ == '__main__':
    print(ItA(27, False))
elif __name__ == '____':
    print(ord('Z'))
    print(chr(91))
elif __name__ == '____':
    a = 'X20'
    print(SIsplit(a))
elif __name__ == '____':
    a = ['X20', 'AT20']
    r = AtI(pickalpha(a))
    print(r)
elif __name__ == '____':
    print(f'ati("AAA"): {AtI("AAA")}')
    print(f'pickalpha("X20"): {pickalpha("X20")}')
    print(f'pickalpha(["X20", "AT20"]): {pickalpha(["X20", "AT20"])}')
