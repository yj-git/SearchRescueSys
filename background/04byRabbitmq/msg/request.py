class MsgRequest:
    '''
        作为job不同步骤之间传递的消息
    '''

    # dict_params=[]
    def __init__(self):
        # 灵感来源自django request中的 content_params
        self.content_params = dict()

    def set_content_type_params(self, key: str, content):
        '''
            判断content_type_params中是否已经存在指定的params
        :return:
        '''
        if self.content_params is not None:
            # self.content_params.update(val=content)
            self.content_params[key] = content
        else:
            self.content_params = dict()
            # if self.content_params.get(key) is not None:
            #     # 若已经存在，则重新赋值
            #     self.content_params.update(key=content)
            # else:
            #     self.content_params

    def get_content_type_params(self, key: str):
        '''
            根据key从 content_params 中找到对应的 obj
        :param key:
        :return:
        '''
        if self.content_params.get(key) is not None:
            return self.content_params.get(key)
        else:
            return None
