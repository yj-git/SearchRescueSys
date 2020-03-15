from catalog import CatalogFactory
# from geoserver.catalog import Catalog
from geoserver.workspace import Workspace
import sys

# TODO:[-] 20-03-12 此处使用修改后的gsconfig
BUILD_SRC = r'D:\01proj\源码\gsconfig'
# BUILD_SRC = r'/Users/evaseemefly/Documents/01Proj/部分源码/gis/gsconfig'
sys.path.append(BUILD_SRC)
from src.geoserver.catalog import Catalog
from src.geoserver.layer import CoverageLayer


def main():
    # cat = CatalogFactory()
    # cat.connect()
    # ws = cat.get_workspace('my_test_2')
    # ws_name: str = 'ceshi'
    ws_name: str = 'my_test_2'
    cat: Catalog = Catalog("http://localhost:8082/geoserver/rest", username="admin", password="geoserver")
    # ws = cat.get_workspaces()
    # TODO:[*] 20-03-13 此处存在的问题是若不存在 指定的ws 链接并不会中断一直链接状态
    ws: Workspace = cat.get_workspace(ws_name)
    # cat.create_ncstore('nmefc_2016072112_opdr', 'my_test_2', 'nmefc/waterwind')
    store_temp = cat.get_store('nmefc_2016072112_opdr', workspace=ws)

    # 测试一下 CoverageLayer
    coverage=CoverageLayer(cat,'ceshi')
    coverage.insert_node({'key':'nativeName','val':'ceshi'})


    # mac
    # store_temp = cat.get_store('nmefc_wind', workspace=ws)
    cat.create_coveragestore('nmefc_2016072112_opdr_02', ws, path=r'file:nmefc/waterwind/nmefc_2016072112_opdr.nc',
                             layer_name='nmefc_2016072112_opdr_02',
                             source_name='x_wind_10m',
                             type='NetCDF')
    cat.create_coverage('my_test_2', 'ceshi_coverage_01', 'nmefc_2016072112_opdr')
    pass


if __name__ == '__main__':
    main()
