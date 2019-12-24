from core.Job import JobRun, change_rate, store_job_rate
from msg.request import MsgRequest


class JobOil(JobRun):
    '''
        注意将所有的job实现类放在了@/job/中
    '''
    _do_funcs = []
    '''
        一个溢油case
    '''

    def do_job(self, **kwargs):
        '''
            搜救的case主要流程:
                1- 根据传入的参数，执行脚本文件
                2- 将传入的参数写入数据库
                3- 过一段时间去指定路径下获取指定名称的nc文件
                4- 将nc文件写入数据库
                TODO:[*] 19-12-17
                准备将所需的步骤加入一个数组中(此处需注意需要统一传入的参数——或者使用*args,**kwargs）
        :return:
        '''
        request = MsgRequest()
        # self._do_funcs.append(self.do_requsest)
        self._do_funcs = [self.get_request, self.do_requsest, self.do_writein_db, self.do_match_targetfile,
                          self.do_store_model, self.do_end]
        # 由于所有需要do job的方法签名是一样的
        for func in self._do_funcs:
            func(request)
        # self.do_requsest(request)

    def get_request(self, request: MsgRequest):
        '''
            获取传过来的 request
        :param request:
        :return:
        '''
        print(f'现在执行的是:[get_request]')
        pass

    @change_rate(rate=10)
    @store_job_rate()
    def do_requsest(self, request: MsgRequest, *args, **kwargs):
        '''
            根据传入的参数执行脚本文件
        :param request:
        :return:
        '''
        oil_pattern: OilPatternMidModel = request.get_content_type_params('oil_pattern')
        # TODO:[*] 19-11-28 下面只是模拟调用脚本的步骤
        print(oil_pattern)
        print(f'现在执行的是:1-[do_requsest]')
        # 执行之后，向request中写入进度
        # 此处放在装饰器中，不在此处
        # request.set_content_type_params('rate', 0.2)

    @change_rate(rate=50)
    @store_job_rate()
    def do_writein_db(self, request: MsgRequest, *args, **kwargs):
        '''
            将传入的oil_pattern 状态写入数据库
        :param request:
        :return:
        '''
        print(f'现在执行的是:2-[do_writein_db]')
        pass

    @change_rate(rate=70)
    @store_job_rate()
    def do_match_targetfile(self, request: MsgRequest, *args, **kwargs):
        '''
            定时去指定目录下判断指定文件是否存在
                注意其中需要加入定时器
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        print(f'现在执行的是:3-[do_match_targetfile]')
        pass

    @change_rate(rate=90)
    @store_job_rate()
    def do_store_model(self, request: MsgRequest, *args, **kwargs):
        '''
            将nc文件写入数据库
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        print(f'现在执行的是:4-[do_store_model]')
        pass

    @change_rate(rate=100)
    @store_job_rate()
    def do_end(self, request: MsgRequest):
        '''
            当前得作业结束
        :param request:
        :return:
        '''
        print(f'现在执行的是:5-[do_end]')
