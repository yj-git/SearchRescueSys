class SimpleValMidModel:
    '''
        潮位站的实时数据与实践 mid model
    '''
    __slots__ = ['val']

    def __init__(self, val: float):
        self.val = val

class SimpleDirValMidModel:
    __slots__ = ['val']

    def __init__(self, val: object):
        self.val = val