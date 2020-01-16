class OilDbReader:
    def read(self):
        pass

    def read_avg_track(self,code):
        '''
            根据传入的code获取指定code的平均轨迹
        :param code:
        :return:
        '''

class OilFileReader:
    def read(self):
        pass


def create_reader(type: str):
    if type == 'db':
        return OilDbReader
    elif type == 'file':
        return OilFileReader

class OilBaseView:
    def get_mearn(self,factor:str,uid:int,):
        '''

        :param factor:
        :return:
        '''