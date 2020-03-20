from datetime import datetime, timedelta
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.models.openoil import OpenOil


class ForecastJob(object):
    CHOICE_TYPE = {
        0: 'CaseOilInfo',
        1: 'CaseRescueInfo'
    }

    def RunOilCase(self, type: CHOICE_TYPE, attrs: dict):
        return None