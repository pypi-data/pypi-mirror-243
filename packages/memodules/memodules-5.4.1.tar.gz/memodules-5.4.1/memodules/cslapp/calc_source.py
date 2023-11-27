from console import clear as cls
flg = True
mode = None
while flg:
    flg = False
    cls()
    print('1- A : B = C : x')
    mode = int(input('mode select:\n'))
    if mode == '':
        flg = True
cls()
if mode == 1:
    print('Mode Number Please')
    print('A : B = C : x')
    a = int(input('A = ?\n'))
    b = int(input('B = ?\n'))
    c = int(input('C = ?\n'))
    print('Solve and Answer')
    print(f'\t{a}x = {b}・{c}')
    print(f'\t{a}x = {b * c}')
    print(f'\t\033[92mx = {(b * c) / a}\033[0m')
