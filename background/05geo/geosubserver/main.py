from catalog import CatalogFactory
# from geoserver.catalog import Catalog
from geoserver.workspace import Workspace
import sys

# TODO:[-] 20-03-12 此处使用修改后的gsconfig
BUILD_SRC = r'D:\01proj\源码\gsconfig'
sys.path.append(BUILD_SRC)
from src.geoserver.catalog import Catalog


def main():
    # cat = CatalogFactory()
    # cat.connect()
    # ws = cat.get_workspace('my_test_2')
    cat: Catalog = Catalog("http://localhost:8082/geoserver/rest", username="admin", password="geoserver")
    # ws = cat.get_workspaces()
    ws: Workspace = cat.get_workspace('my_test_2')
    # cat.create_ncstore('nmefc_2016072112_opdr', 'my_test_2', 'nmefc/waterwind')
    store_temp = cat.get_store('nmefc_2016072112_opdr', ws)
    cat.create_coveragestore('nmefc_2016072112_opdr_02', ws, path=r'file:nmefc/waterwind/nmefc_2016072112_opdr.nc',
                             type='NetCDF')
    cat.create_coverage('my_test_2', 'ceshi_coverage_01', 'nmefc_2016072112_opdr')
    pass


if __name__ == '__main__':
    main()
