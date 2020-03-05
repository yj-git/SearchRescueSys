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
			"name": "SearchRescue:nmefc_wind_dir_xy",
			"href": "http:\/\/localhost:8082\/geoserver\/rest\/workspaces\/SearchRescue\/coveragestores\/nmefc_wind_dir_xy.json"
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
    headers_xml_json = {'Content-Type': 'application/json'}
    response = requests.post(
        f'http://localhost:8082/geoserver/rest/workspaces/{WORK_SPACE}/coveragestores/{coveragestore}/coverages',
        auth=('admin', 'geoserver'),
        # TODO:[*] 20-03-05 此处的问题是对于一个栅格数据有多个特征时，如何添加 对应的name
        # data='<coverage><nativeCoverageName>x_wind_10m</nativeCoverageName><name>x_wind_10m</name></coverage><coverage><nativeCoverageName>y_wind_10m</nativeCoverageName><name>x_wind_10m</name></coverage>',
        data=json_str,
        headers=headers_xml)
    pass


if __name__ == '__main__':
    main()
