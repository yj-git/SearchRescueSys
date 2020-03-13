from requests.models import Response
import xml.etree.ElementTree as ET
from geoserver.catalog import Catalog
from geoserver.catalog import FailedRequestError
from conf.settings import CATALOG


class CatalogFactory(Catalog):
    '''
        此类只是工具类，不提供实际的业务逻辑
        需要新实现的逻辑有：
            1- 创建 nc store
        需要封装调用gsconfig的逻辑：
            1- 创建工作区
            2- 提交图层
            3- 绑定style
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
    def base_url(self):
        '''
            获取 url:http://localhost:8082
                _geo_perfix:geoserver/rest
                拼接后的结果
        :return:
        '''
        merage_url = '/'.join([self.url, self._geo_perfix])
        return merage_url

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

    def get_coverage(self,work_space:str,store:str):
        '''
            api：
                https://docs.geoserver.org/latest/en/api/#1.0.0/coverages.yaml
        :param work_space:
        :param store:
        :return:
        '''
        pass


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
            TODO:[-] 20-03-10 已完成
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

        # TODO:[*] 以下由于有空格引起了异常，建议加入提出空格的操作
        data = f'<coverageStore><name>{store_name} </name><workspace> {workspace}</workspace><enabled>true</enabled><type>NetCDF</type><url>{file_path} </url></coverageStore>'
        # data_bak = data_bak.replace(' ', '')
        data = ''.join(data.split())
        # data = '<coverageStore><name>' + store_name + '</name><workspace>' + workspace + "</workspace><enabled>true</enabled><type>NetCDF</type><url>" + file_path + '</url></coverageStore>'
        # print(data)
        url = f'{self.geo_url}/workspaces/{workspace}/coveragestores?configure=all'
        header = {'content-type': 'text/xml'}
        # TODO:[*] 20-03-09 注意此处直接调用 -> catalog ->http_request 会提示没有client的错误，client保存的是 session
        super().__init__(self.base_url, self.username, self.pwd)
        # TODO:[*] 20-03-10  ERROR [geoserver.rest] - Store must be part of a workspace
        # 此处调用父类的 http_requset 方法
        res = self.http_request(url, method='post', data=data, headers=header)  # type:Response
        if res.status_code not in [200, 201]:
            # TODO:[-] 20-03-10 此处参考了一下 gsconfig -> catalog -> create_coveragestore 的源码
            FailedRequestError(f'提交 nc store 错误,url:{url}|name:{name}')
        pass

    def create_coverage(self, work_space: str = None, coverage_title: str = None, store_name: str = None):
        # 尝试一下将 xml str -> xml
        xml_str = f'''
<coverage>
  <name>ceshi_coverage_01</name>
  <nativeName>ceshi_coverage_01</nativeName>
  <namespace>
    <name>my_test_2</name>
    <atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="http://localhost:8082/geoserver/rest/namespaces/my_test_2.xml" type="application/xml"/>
  </namespace>
  <title>ceshi_coverage_01</title>
  <description>Generated from NetCDF</description>
  <keywords>
    <string>ceshi_coverage_01</string>
    <string>WCS</string>
    <string>NetCDF</string>
  </keywords>
  <nativeCRS>GEOGCS["WGS 84", DATUM["World Geodetic System 1984", SPHEROID["WGS 84", 6378137.0, 298.257223563, AUTHORITY["EPSG","7030"]], AUTHORITY["EPSG","6326"]], PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]], UNIT["degree", 0.017453292519943295], AXIS["Geodetic longitude", EAST], AXIS["Geodetic latitude", NORTH], AUTHORITY["EPSG","4326"]]</nativeCRS>
  <srs>EPSG:4326</srs>
  <projectionPolicy>REPROJECT_TO_DECLARED</projectionPolicy>
  <enabled>true</enabled>
  <metadata>
    <entry key="COVERAGE_VIEW">
      <coverageView>
        <coverageBands>
          <coverageBand>
            <inputCoverageBands class="singleton-list">
              <inputCoverageBand>
                <coverageName>x_wind_10m</coverageName>
              </inputCoverageBand>
            </inputCoverageBands>
            <definition>x_wind_10m</definition>
            <index>0</index>
            <compositionType>BAND_SELECT</compositionType>
          </coverageBand>
          <coverageBand>
            <inputCoverageBands class="singleton-list">
              <inputCoverageBand>
                <coverageName>y_wind_10m</coverageName>
              </inputCoverageBand>
            </inputCoverageBands>
            <definition>y_wind_10m</definition>
            <index>1</index>
            <compositionType>BAND_SELECT</compositionType>
          </coverageBand>
        </coverageBands>
        <name>ceshi_coverage_01</name>
        <envelopeCompositionType>INTERSECTION</envelopeCompositionType>
        <selectedResolution>BEST</selectedResolution>
        <selectedResolutionIndex>-1</selectedResolutionIndex>
      </coverageView>
    </entry>
    <entry key="cachingEnabled">false</entry>
    <entry key="dirName">nmefc_wind_dir_xy_view_nmefc_wind</entry>
  </metadata>
  <store class="coverageStore">
    <name>my_test_2:nmefc_2016072112_opdr</name>
    <atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="http://localhost:8082/geoserver/rest/workspaces/my_test_2/coveragestores/nmefc_2016072112_opdr.xml" type="application/xml"/>
  </store>
  <nativeFormat>NetCDF</nativeFormat>
  <grid dimension="2">
    <range>
      <low>0 0</low>
      <high>251 251</high>
    </range>
    <transform>
      <scaleX>0.2</scaleX>
      <scaleY>-0.2</scaleY>
      <shearX>0.0</shearX>
      <shearY>0.0</shearY>
      <translateX>100.0</translateX>
      <translateY>50.0</translateY>
    </transform>
    <crs>EPSG:4326</crs>
  </grid>
  <supportedFormats>
    <string>GEOTIFF</string>
    <string>GIF</string>
    <string>PNG</string>
    <string>JPEG</string>
    <string>TIFF</string>
  </supportedFormats>
  <defaultInterpolationMethod>nearest neighbor</defaultInterpolationMethod>
  <dimensions>
    <coverageDimension>
      <name>x_wind_10m</name>
      <description>GridSampleDimension[-Infinity,Infinity]</description>
      <range>
        <min>-inf</min>
        <max>inf</max>
      </range>
      <dimensionType>
        <name>REAL_32BITS</name>
      </dimensionType>
    </coverageDimension>
    <coverageDimension>
      <name>y_wind_10m</name>
      <description>GridSampleDimension[-Infinity,Infinity]</description>
      <range>
        <min>-inf</min>
        <max>inf</max>
      </range>
      <dimensionType>
        <name>REAL_32BITS</name>
      </dimensionType>
    </coverageDimension>
  </dimensions>
  <requestSRS>
    <string>EPSG:4326</string>
  </requestSRS>
  <responseSRS>
    <string>EPSG:4326</string>
  </responseSRS>
  <parameters>
    <entry>
      <string>Bands</string>
      <null/>
    </entry>
    <entry>
      <string>Filter</string>
      <null/>
    </entry>
  </parameters>
  <nativeCoverageName>ceshi_coverage_01</nativeCoverageName>
</coverage>
                
        '''

        #         xml_str = f'''<coverage>
        #   <name>{coverage_title}</name>
        #   <nativeName>{coverage_title}</nativeName>
        #   <namespace>
        #     <name>{work_space}</name>
        #     <atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="http://localhost:8082/geoserver/rest/namespaces/{work_space}.xml" type="application/xml"/>
        #   </namespace>
        #   <title>{coverage_title}</title>
        #   <description>Generated from NetCDF</description>
        #   <keywords>
        #     <string>{coverage_title}</string>
        #     <string>WCS</string>
        #     <string>NetCDF</string>
        #   </keywords>
        #   <nativeCRS>GEOGCS["WGS 84", DATUM["World Geodetic System 1984", SPHEROID["WGS 84", 6378137.0, 298.257223563, AUTHORITY["EPSG","7030"]], AUTHORITY["EPSG","6326"]], PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]], UNIT["degree", 0.017453292519943295], AXIS["Geodetic longitude", EAST], AXIS["Geodetic latitude", NORTH], AUTHORITY["EPSG","4326"]]</nativeCRS>
        #   <srs>EPSG:4326</srs>
        #   <nativeBoundingBox>
        #     <minx>99.9</minx>
        #     <maxx>150.10000000000002</maxx>
        #     <miny>-0.1</miny>
        #     <maxy>50.1</maxy>
        #     <crs>EPSG:4326</crs>
        #   </nativeBoundingBox>
        #   <latLonBoundingBox>
        #     <minx>99.9</minx>
        #     <maxx>150.10000000000002</maxx>
        #     <miny>-0.1</miny>
        #     <maxy>50.1</maxy>
        #     <crs>EPSG:4326</crs>
        #   </latLonBoundingBox>
        #   <projectionPolicy>REPROJECT_TO_DECLARED</projectionPolicy>
        #   <enabled>true</enabled>
        #   <metadata>
        #     <entry key="COVERAGE_VIEW">
        #       <coverageView>
        #         <coverageBands>
        #           <coverageBand>
        #             <inputCoverageBands class="singleton-list">
        #               <inputCoverageBand>
        #                 <coverageName>x_wind_10m</coverageName>
        #               </inputCoverageBand>
        #             </inputCoverageBands>
        #             <definition>x_wind_10m</definition>
        #             <index>0</index>
        #             <compositionType>BAND_SELECT</compositionType>
        #           </coverageBand>
        #           <coverageBand>
        #             <inputCoverageBands class="singleton-list">
        #               <inputCoverageBand>
        #                 <coverageName>y_wind_10m</coverageName>
        #               </inputCoverageBand>
        #             </inputCoverageBands>
        #             <definition>y_wind_10m</definition>
        #             <index>1</index>
        #             <compositionType>BAND_SELECT</compositionType>
        #           </coverageBand>
        #         </coverageBands>
        #         <name>{coverage_title}</name>
        #         <envelopeCompositionType>INTERSECTION</envelopeCompositionType>
        #         <selectedResolution>BEST</selectedResolution>
        #         <selectedResolutionIndex>-1</selectedResolutionIndex>
        #       </coverageView>
        #     </entry>
        #     <entry key="cachingEnabled">false</entry>
        #     <entry key="dirName">nmefc_wind_dir_xy_view_nmefc_wind</entry>
        #   </metadata>
        #   <store class="coverageStore">
        #     <name>{work_space}:{store_name}</name>
        #     <atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="http://localhost:8082/geoserver/rest/workspaces/{work_space}/coveragestores/{store_name}.xml" type="application/xml"/>
        #   </store>
        #   <nativeFormat>NetCDF</nativeFormat>
        #   <grid dimension="2">
        #     <range>
        #       <low>0 0</low>
        #       <high>251 251</high>
        #     </range>
        #     <transform>
        #       <scaleX>0.2</scaleX>
        #       <scaleY>-0.2</scaleY>
        #       <shearX>0.0</shearX>
        #       <shearY>0.0</shearY>
        #       <translateX>100.0</translateX>
        #       <translateY>50.0</translateY>
        #     </transform>
        #     <crs>EPSG:4326</crs>
        #   </grid>
        #   <supportedFormats>
        #     <string>GEOTIFF</string>
        #     <string>GIF</string>
        #     <string>PNG</string>
        #     <string>JPEG</string>
        #     <string>TIFF</string>
        #   </supportedFormats>
        #   <interpolationMethods>
        #     <string>nearest neighbor</string>
        #     <string>bilinear</string>
        #     <string>bicubic</string>
        #   </interpolationMethods>
        #   <defaultInterpolationMethod>nearest neighbor</defaultInterpolationMethod>
        #   <dimensions>
        #     <coverageDimension>
        #       <name>x_wind_10m</name>
        #       <description>GridSampleDimension[-Infinity,Infinity]</description>
        #       <range>
        #         <min>-inf</min>
        #         <max>inf</max>
        #       </range>
        #       <dimensionType>
        #         <name>REAL_32BITS</name>
        #       </dimensionType>
        #     </coverageDimension>
        #     <coverageDimension>
        #       <name>y_wind_10m</name>
        #       <description>GridSampleDimension[-Infinity,Infinity]</description>
        #       <range>
        #         <min>-inf</min>
        #         <max>inf</max>
        #       </range>
        #       <dimensionType>
        #         <name>REAL_32BITS</name>
        #       </dimensionType>
        #     </coverageDimension>
        #   </dimensions>
        #   <requestSRS>
        #     <string>EPSG:4326</string>
        #   </requestSRS>
        #   <responseSRS>
        #     <string>EPSG:4326</string>
        #   </responseSRS>
        #   <parameters>
        #     <entry>
        #       <string>Bands</string>
        #       <null/>
        #     </entry>
        #     <entry>
        #       <string>Filter</string>
        #       <null/>
        #     </entry>
        #   </parameters>
        #   <nativeCoverageName>{coverage_title}</nativeCoverageName>
        # </coverage>
        #                 '''

        # coverage_xml_path = r'./template/coverage.xml'
        # 注意此处会存在问题，需要剔除掉换行符,剔除掉空格
        # xml_str = xml_str.replace("\n", '')
        # xml_str = ''.join(xml_str.split())
        # et = ET.ElementTree(file=coverage_xml_path)
        parser = ET.XMLParser(encoding="utf-8")
        # TODO:[-] 直接从字符串中解析
        # TODO:[*] 此处出现一个问题：xml.etree.ElementTree.ParseError: not well-formed (invalid token): line 1, column 65
        # xml = ET.fromstring(xml_str,parser=parser)
        # xml1=ET.XML(xml_str)
        # TODO:[*] 在.xml中加入占位符读取后填充如何操作？
        # xml = ET.parse(xml_str)

        # http: // localhost: 8082 / geoserver / rest / workspaces /
        url = f'{self.base_url}/workspaces/{work_space}/coveragestores/{coverage_title}/coverages'
        data = xml_str
        header = {'content-type': 'text/xml'}
        super().__init__(self.base_url, self.username, self.pwd)
        res = self.http_request(url, method='post', data=data, headers=header)
        pass

    def binding_coverage_style(self,work_space:str,coverage_title:str,sld:str=None,style:str=None):
        '''
            为指定coverage 绑定指定style (sld)
        :param work_space:
        :param coverage_title:
        :param sld:
        :param style:
        :return:
        '''
        # 为指定coverage 绑定指定style (sld)

        '''
            大体流程：
                1- 查找指定work_space
                2- 查找指定coverage
                以上只要有不存在则抛出异常
                3- 根据传入的sld或style
        '''
        if self.get_workspace(work_space) is not None:
            pass
        # if self.get_coverage(work_space,)

