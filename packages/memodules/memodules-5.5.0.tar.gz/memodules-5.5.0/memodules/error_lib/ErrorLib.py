class ModeSelectionError(Exception):
    """Error when there is a mode that does not exist in the 'mode=' arguments"""
    def __str__(self):
        return 'Selecting a Mode That Doesn\'t Exist'
    
def modeselectionerror():
    raise ModeSelectionError