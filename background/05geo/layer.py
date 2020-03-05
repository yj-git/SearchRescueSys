import os
import requests
from geoserver.catalog import Catalog

# 用户名及密码
USER_NAME = 'admin'
PWD = 'geoserver'

URL = 'http://localhost:8082'
GEO_PERFIX = 'geoserver/rest'
WORK_SPACE = 'my_test_2'

url = '/'.join([URL, GEO_PERFIX])


def main():
    # 主要使用 gsconfig 实现
    # 1- 创建指定的命名空间
    #
    cat = Catalog(url, username=USER_NAME, password=PWD)
    ws = cat.create_workspace(WORK_SPACE, WORK_SPACE)
    # 2- TODO:[*] 创建store——暂时放弃使用 catalog create的方式，还是直接rest的方式
    # ds=cat.create_datastore('testStore',WORK_SPACE)
    # ds.connection_parameters.update()
    # 2- 提交store存储
    coveragestore = 'st_3'
    headers_xml = {'content-type': 'text/xml'}
    # TODO:[*] 20-03-04 注意此处存在的问题： 若提交非geoserver 服务所在的路径下的data，会提示错误
    file_path = r'file:nmefc/waterwind/nmefc_2016072112_opdr.nc'
    # 注意 f-string 多行也适用
    store_xml=f'''
                <coverageStore>
                    <name>{coveragestore}</name>
                    <description>风场处理后的数据</description>
                    <type>NetCDF</type>
                    <enabled>true</enabled>
                    <workspace>
                        <name>{WORK_SPACE}</name>                        
                    </workspace>
                    <__default>false</__default>
                    <url>file:{file_path}</url>
                    <coverages>                        
                    </coverages>
                </coverageStore>
              '''
    r_create_coveragestore = requests.post(
        f'http://localhost:8082/geoserver/rest/workspaces/{WORK_SPACE}/coveragestores?configure=all',
        auth=('admin', 'geoserver'),
        data='<coverageStore><name>' + coveragestore + '</name><workspace>' + WORK_SPACE + "</workspace><enabled>true</enabled><type>NetCDF</type><url>" + file_path + '</url></coverageStore>',
        headers=headers_xml)
    # 参考：
    # https: // geoserver.geo - solutions.it / edu / en / rest / python_gsconfig.html
    geosolutions = cat.get_workspace(WORK_SPACE)
    import geoserver.util

    # 3- 提交netcdf的图层
    json_str_2= '''
    {
	"coverage": {
		"name": "ceshi_0305_03",
		"nativeName": "ceshi_0305_03",		
		"title": "ceshi_0305_03",		
		"metadata": {
			"entry": [{
				"@key": "COVERAGE_VIEW",
				"coverageView": {
					"coverageBands": {
						"coverageBand": [{
							"inputCoverageBands": {
								"@class": "singleton-list",
								"inputCoverageBand": [{
									"coverageName": "x_wind_10m"
								}]
							},
							"definition": "x_wind_10m",
							"index": 0,
							"compositionType": "BAND_SELECT"
						},
						 {
							"inputCoverageBands": {
								"@class": "singleton-list",
								"inputCoverageBand": [{
									"coverageName": "y_wind_10m"
								}]
							},
							"definition": "y_wind_10m",
							"index": 1,
							"compositionType": "BAND_SELECT"
						}]
					},
					"name": "ceshi_0305_03",
					"envelopeCompositionType": "INTERSECTION",
					"selectedResolution": "BEST",
					"selectedResolutionIndex": -1
				}
			}, {
				"@key": "cachingEnabled",
				"$": "false"
			}, {
				"@key": "dirName",
				"$": "nmefc_wind_dir_xy_ceshi_0305_03
			}]
		},
		"store": {
			"@class": "coverageStore",
			"name": "{WORK_SPACE}:{store_name}",
			"href": "http:\/\/localhost:8082\/geoserver\/rest\/workspaces\/{WORK_SPACE}\/coveragestores\/{store_name}.json"
		},
		"nativeFormat": "NetCDF",
		
		"supportedFormats": {
			"string": ["GEOTIFF", "GIF", "PNG", "JPEG", "TIFF"]
		},
		"interpolationMethods": {
			"string": ["nearest neighbor", "bilinear", "bicubic"]
		},
		"defaultInterpolationMethod": "nearest neighbor",
		"dimensions": {
			"coverageDimension": [{
				"name": "x_wind_10m",
				"description": "GridSampleDimension[-Infinity,Infinity]",
				"range": {
					"min": "-inf",
					"max": "inf"
				},
				"dimensionType": {
					"name": "REAL_32BITS"
				}
			}, {
				"name": "y_wind_10m",
				"description": "GridSampleDimension[-Infinity,Infinity]",
				"range": {
					"min": "-inf",
					"max": "inf"
				},
				"dimensionType": {
					"name": "REAL_32BITS"
				}
			}]
		},
		"requestSRS": {
			"string": ["EPSG:4326"]
		},
		"responseSRS": {
			"string": ["EPSG:4326"]
		},
		"parameters": {
			"entry": [{
				"string": "Bands",
				"null": ""
			}, {
				"string": "Filter",
				"null": ""
			}]
		},
		"nativeCoverageName": "ceshi_0305_03"
	}
}
    '''

    # TODO:[-] 20-03-05 此种方式可以提交，但只有一路band
    json_str='''
                <coverage>
                <title>st_4</title>
                <name>st_4</name>
                <metadata>
                    <entry key="time">
                         <coverageView>
                            <coverageBands>
                                <coverageBand>
                                        <inputCoverageBands>
                                            <inputCoverageBand>
                                                <coverageName>x_wind_10m</coverageName>
                                            </inputCoverageBand>
                                        </inputCoverageBands>
                                    <definition>x_wind_10m</definition>
                                    <index>0</index>
                                    <compositionType>BAND_SELECT</compositionType>
                                </coverageBand>
                            </coverageBands>
                        </coverageView>
                    </entry>
                </metadata>
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
                <enabled>true</enabled>
                <dimensions>
                    <coverageDimension>
                        <name>x_wind_10m</name>          
                        <dimensionType>
                            <name>REAL_32BITS</name>
                        </dimensionType>              
                    </coverageDimension>
                    <coverageDimension>
                        <name>y_wind_10m</name>      
                        <dimensionType>
                            <name>REAL_32BITS</name>
                        </dimensionType>                       
                    </coverageDimension>
                </dimensions>
                <nativeFormat>NetCDF</nativeFormat>
                <defaultInterpolationMethod>nearest neighbor</defaultInterpolationMethod>
                <srs>EPSG:4326</srs>
                <requestSRS>
                    <string>EPSG:4326</string>
                </requestSRS>
                <responseSRS>
                    <string>EPSG:4326</string>
                </responseSRS>
                <nativeCoverageName>x_wind_10m</nativeCoverageName>
            </coverage>
            '''
    # json_str = '''<coverage>
    #                 <title>{coveragestore}</title>
    #                 <metadata>
    #                     <entry key="time">
    #                         <dimensionInfo>
    #                         <enabled>true</enabled>
    #                         <attribute>time_attribute</attribute>
    #                         <presentation>LIST</presentation>
    #                         <units>ISO8601</units>
    #                         <defaultValue>NONE</defaultValue>
    #                         </dimensionInfo>
    #                         <coverageView>
    #                             <coverageBands>
    #                                 <inputCoverageBands>
    #                                     <inputCoverageBand>
    #                                         <coverageName>wind</coverageName>
    #                                     </inputCoverageBand>
    #                                 </inputCoverageBands>
    #                                 <definition>x_wind_10m</definition>
    #                                 <index>0</index>
    #                             </coverageBands>
    #                         </coverageView>
    #                     </entry>
    #                 </metadata>
    #                 <enabled>true</enabled>
    #             </coverage>
    #             '''
    #
    #
    # data = {
    #     'a': 123,
    #     'b': 123
    # }
    # import json
    # json_temp = json.dumps(data)


    coverage_title='ceshi_coverage_01'
    store_name='st_3'
    json_coverage_new=f'''
    <coverage>
  <name>{coverage_title}</name>
  <nativeName>{coverage_title}</nativeName>
  <namespace>
    <name>{WORK_SPACE}</name>
    <atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="http://localhost:8082/geoserver/rest/namespaces/{WORK_SPACE}.xml" type="application/xml"/>
  </namespace>
  <title>{coverage_title}</title>
  <description>Generated from NetCDF</description>
  <keywords>
    <string>{coverage_title}</string>
    <string>WCS</string>
    <string>NetCDF</string>
  </keywords>
  <nativeCRS>GEOGCS["WGS 84", DATUM["World Geodetic System 1984", SPHEROID["WGS 84", 6378137.0, 298.257223563, AUTHORITY["EPSG","7030"]], AUTHORITY["EPSG","6326"]], PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]], UNIT["degree", 0.017453292519943295], AXIS["Geodetic longitude", EAST], AXIS["Geodetic latitude", NORTH], AUTHORITY["EPSG","4326"]]</nativeCRS>
  <srs>EPSG:4326</srs>
  <nativeBoundingBox>
    <minx>99.9</minx>
    <maxx>150.10000000000002</maxx>
    <miny>-0.1</miny>
    <maxy>50.1</maxy>
    <crs>EPSG:4326</crs>
  </nativeBoundingBox>
  <latLonBoundingBox>
    <minx>99.9</minx>
    <maxx>150.10000000000002</maxx>
    <miny>-0.1</miny>
    <maxy>50.1</maxy>
    <crs>EPSG:4326</crs>
  </latLonBoundingBox>
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
        <name>{coverage_title}</name>
        <envelopeCompositionType>INTERSECTION</envelopeCompositionType>
        <selectedResolution>BEST</selectedResolution>
        <selectedResolutionIndex>-1</selectedResolutionIndex>
      </coverageView>
    </entry>
    <entry key="cachingEnabled">false</entry>
    <entry key="dirName">nmefc_wind_dir_xy_view_nmefc_wind</entry>
  </metadata>
  <store class="coverageStore">
    <name>{WORK_SPACE}:{store_name}</name>
    <atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="http://localhost:8082/geoserver/rest/workspaces/{WORK_SPACE}/coveragestores/{store_name}.xml" type="application/xml"/>
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
  <interpolationMethods>
    <string>nearest neighbor</string>
    <string>bilinear</string>
    <string>bicubic</string>
  </interpolationMethods>
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
  <nativeCoverageName>{coverage_title}</nativeCoverageName>
</coverage>
                        '''
    headers_xml_json = {'Content-Type': 'application/json'}
    response = requests.post(
        f'http://localhost:8082/geoserver/rest/workspaces/{WORK_SPACE}/coveragestores/{coveragestore}/coverages',
        auth=('admin', 'geoserver'),
        # TODO:[*] 20-03-05 此处的问题是对于一个栅格数据有多个特征时，如何添加 对应的name
        # data='<coverage><nativeCoverageName>x_wind_10m</nativeCoverageName><name>x_wind_10m</name></coverage><coverage><nativeCoverageName>y_wind_10m</nativeCoverageName><name>x_wind_10m</name></coverage>',
        data=json_coverage_new,
        headers=headers_xml)
    pass

    # 5 绑定样式
    style_name='wind_dir_style'
    json_style=f'''
                    <defaultStyle>
                        <name>{WORK_SPACE}:{style_name}</name>
                        <workspace>{WORK_SPACE}</workspace>
                        <atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="http://localhost:8082/geoserver/rest/workspaces/{WORK_SPACE}/styles/{style_name}.xml" type="application/xml"/>
                    </defaultStyle>
                '''
    response=requests.post(
        f'http://localhost:8082/geoserver/rest/layers/{coverage_title}',
        auth=('admin', 'geoserver'),
        data=json_style,
        headers=headers_xml)

if __name__ == '__main__':
    main()
