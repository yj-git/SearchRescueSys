from geoserver.catalog import Catalog
from conf.settings import CATALOG


class CatalogFactory(Catalog):
    '''

    '''

    # _catalog = None

    def __init__(self, username=CATALOG.get('username'), pwd=CATALOG.get('pwd'), url=CATALOG.get('geo_url'),
                 work_space=CATALOG.get('work_space')):
        '''
            Catalog的构造函数，主要用来获取 登录 geoserver 的 name，pwd，url
        :param username:
        :param pwd:
        '''
        self.username = username
        self.pwd = pwd
        self.url = url
        self.work_space = work_space
        self._geo_perfix = 'geoserver/rest'
        assert None not in [self.username, self.pwd, self.url, self.work_space], '初始化失败'
        self._cat = None  # type:Catalog

    @property
    def geo_url(self):
        '''
            拼接后的geo_url
        :return:
        '''
        merage_url = '/'.join([self.url, self._geo_perfix])
        return merage_url

    def connect(self):
        '''
            连接器
        :return:
        '''
        if self._cat is None:
            self._cat = Catalog(self.geo_url, username=self.username, password=self.pwd)

        return

    def get_workspace(self, work_space: str):
        '''
            获取指定work_space
        :param work_space:
        :return:
        '''
        work_space_temp = None
        if self._cat is not None:
            work_space_temp = self._cat.get_workspace(work_space)
        return work_space_temp

    def create_workspace(self, work_space: str):
        '''
            根据传入的work_space名字创建对应的命名空间，
            返回创建后的workspace
        :param work_space:
        :return:
        '''
        ws = self.get_workspace(work_space)
        if not ws:
            ws = self._cat.create_workspace(work_space, work_space)
        return ws

    def create_ncstore(self, name, workspace=None, path=None,
                       create_layer=True, layer_name=None, source_name=None, upload_data=False,
                       ):
        '''
            此处借鉴 catalog.py -> Catalog -> create_coveragestore
        :param name:
        :param workspace:
        :param path:
        :param create_layer:
        :param layer_name:
        :param source_name:
        :param upload_data:
        :return:
        '''

        ws = self.get_workspace(workspace)
        store_name = name
        file_path = f'file:{path}/{name}.nc'

        data = f'<coverageStore><name>{store_name} </name><workspace> {workspace}  </workspace><enabled>true</enabled><type>NetCDF</type><url>{file_path} </url></coverageStore>'
        url = f'{self.geo_url}/workspaces/{workspace}/coveragestores?configure=all'
        header = {'content-type': 'text/xml'}
        # TODO:[*] 20-03-09 注意此处直接调用 -> catalog ->http_request 会提示没有client的错误，client保存的是 session
        
        res = self.http_request(url, method='post', data=data, headers=header)
