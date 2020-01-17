class StartEndDateMidModel:
    __slots__ = ['start', 'end']

    def __init__(self, start, end):
        self.start = start
        self.end = end


class OilSpillingAvgMidModel:
    def __init__(self, code, status, point, time):
        self.code = code
        self.status = status
        self.point = point
        self.time = time
