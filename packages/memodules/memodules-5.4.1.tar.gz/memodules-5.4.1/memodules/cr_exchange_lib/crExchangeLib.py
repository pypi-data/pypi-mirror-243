class NotBoolStrings(Exception):
    """Exception that occurs at the time of A"""
    def __str__(self):
        return 'Not BoolStrings Error'

def strbool(TargetString: str) -> bool:
    lowstr = TargetString.lower()
    if lowstr == 'true':
        return True
    elif lowstr == 'false':
        return False
    else:
        try:
            raise NotBoolStrings
        except NotBoolStrings as e:
            print('Set Arguments isn\'t BoolStrings') 
    
if __name__ == '__main__':
    strbool('tru')