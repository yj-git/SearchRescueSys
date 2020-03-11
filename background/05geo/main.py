# 本地测试 自动化geoserver发布服务
import os
import requests
from geoserver.catalog import Catalog

# 用户名及密码
USER_NAME = 'admin'
PWD = 'geoserver'

URL = 'http://localhost:8082'
GEO_PERFIX = 'geoserver/rest'
WORK_SPACE = 'my_test'

url = '/'.join([URL, GEO_PERFIX])


def main():
    # 注意 url 中暂时不用加入 work_space
    # 参考 gsconfig/examples/same_srs
    # 1- 创建指定的命名空间
    cat = Catalog(url, username=USER_NAME, password=PWD)
    # ws = cat.get_workspace(WORK_SPACE)
    ws = cat.create_workspace(WORK_SPACE, WORK_SPACE)


    # 2- 提交store存储
    coveragestore = 'st_2'
    headers_xml = {'content-type': 'text/xml'}
    # TODO:[*] 20-03-04 注意此处存在的问题： 若提交非geoserver 服务所在的路径下的data，会提示错误
    file_path = r'nmefc/waterwind/nmefc_2016072112_opdr.nc'
    r_create_coveragestore = requests.post(
        f'http://localhost:8082/geoserver/rest/workspaces/{WORK_SPACE}/coveragestores?configure=all',
        auth=('admin', 'geoserver'),
        data='<coverageStore><name>' + coveragestore + '</name><workspace>' + WORK_SPACE + "</workspace><enabled>true</enabled><type>NetCDF</type><url>" + file_path + '</url></coverageStore>',
        headers=headers_xml)

    # 3- 指定样式
    # old_name_layer = "Band1"
    # new_name_layer = "newBand"
    # stylename = 'test'
    # stylefilename = stylename + '.sld'
    # styleallname = 'd:\\ROURPATH\\styles\\' + stylefilename
    #
    # # creates new style
    # r_create_new_style = requests.post("http://localhost:8090/geoserver/rest/styles",
    #                                    auth=('admin', 'geoserver'),
    #                                    data='<style><name>' + stylename + '</name><filename>' + stylefilename + '</filename></style>',
    #                                    headers=headers_xml)
    #
    # # upload new style
    # with open(styleallname, 'rb') as sld_file:
    #     r_upload_new_style = requests.put("http://localhost:8090/geoserver/rest/styles/" + stylename,
    #                                       auth=('admin', 'geoserver'),
    #                                       data=sld_file,
    #                                       headers=headers_sld)
    #
    # # assign it to a layer
    # r_assign_new_style = requests.put("http://localhost:8090/geoserver/rest/layers/" + workspace + ':' + new_name_layer,
    #                                   auth=('admin', 'geoserver'),
    #                                   data='<layer><defaultStyle><name>' + stylename + '</name></defaultStyle></layer>',
    #                                   headers=headers_xml)

    # 4- 发布服务
    # 暂时使用现在的样式 SearchRescue/wind_dir_style
    old_name_layer = "Band1"
    new_name_layer = "newBand"

    # data:<coverage><nativeCoverageName>RH2</nativeCoverageName><name>RH2</name></coverage>
    # url:http://localhost:8090/geoserver/rest/workspaces/cite/coveragestores/netcdfstore/coverages

    # r_change_name = requests.put(
    #     'http://localhost:8090/geoserver/rest/workspaces/' + workspace + "/coveragestores/" + coveragestore + "/coverages/" + old_name_layer,
    #     auth=('admin', 'geoserver'),
    #     data='<coverage><name>' + new_name_layer + '</name><enabled>true</enabled></coverage>',
    #     headers=headers_xml)
    # pass


if __name__ == '__main__':
    main()
