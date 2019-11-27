import os, path


class JobBase:
    '''
        基础的作业父类，所有的作业均要继承此类
    '''

    def __init__(self):
        # 当前的作业的状态
        self.state = ''
        # 数据库中的作业的id
        self.jobid = ''
        # 提交作业的用户的id
        self.userid = ''
        # 创建作业的时间
        self.created = ''
        #
        pass

    def commit(self):
        '''
            执行完当前作业需要更新数据库中状态
        :return:
        '''
        pass


class JobRun(JobBase):
    def __init__(self, userid: str, createdstamp: int, casename: str, dir: str):
        self.userid = userid
        self.created = createdstamp
        self.casename = casename
        self.dir = dir

    @property
    def filename(self):
        '''
            根据 userid,时间戳,case名称组合成一个filename
        :return:
        '''
        parts = [self.userid, str(self.created), self.casename]
        filename = '_'.join(parts)
        return filename

    @property
    def fullpath(self):
        '''
            nc文件的的全路径
        :return:
        '''
        fullpath = os.path.join(self.dir, self.filename)
        return fullpath

    def load(self, msg):
        pass

    def doPy(self):
        '''
            执行脚本文件
        :return:
        '''
        print("模拟执行.py脚本")
        # 会生成一个生成的nc格式的文件

    def
