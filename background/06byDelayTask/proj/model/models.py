from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, text
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey,Sequence,MetaData,Table
from sqlalchemy.orm import relationship,sessionmaker

import os
from datetime import datetime
import xarray as xar
import netCDF4 as nc
import pandas as pd

from conf.settings import DOWNLOAD_ROOT, GEO_CURRENT_ROOT, GEO_WIND_ROOT, _WORK_SPACE
from util.tools import local_to_utc, utc_to_local
engine = create_engine("mysql+mysqldb://root:123456@localhost/searchrescue", encoding='utf-8', echo=True)

# 生成基类
Base = declarative_base()
md = MetaData(bind=engine) #引用MetaData
metadata = Base.metadata

class DictBase(Base):
    __tablename__ = 'dict_base'

    code = Column(Integer, primary_key=True)
    pid = Column(Integer, nullable=False)
    type_code = Column(VARCHAR(20), nullable=False)
    name = Column(VARCHAR(20), nullable=False)
    desc = Column(VARCHAR(200), nullable=False)
    val = Column(VARCHAR(50), nullable=False)

class GeoCoverageinfo(Base):
    __tablename__ = 'geo_coverageinfo'

    is_del = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    id = Column(Integer, primary_key=True)
    root_path = Column(VARCHAR(100), nullable=False)
    relative_path = Column(VARCHAR(100), nullable=False)
    file_name = Column(VARCHAR(50), nullable=False)
    file_size = Column(Float(asdecimal=True), nullable=False)
    create_date = Column(DATETIME(fsp=6))
    dimessions = Column(VARCHAR(500))
    variables = Column(VARCHAR(500))
    desc = Column(VARCHAR(500))
    is_original = Column(TINYINT(1))
    coverage_area = Column(Integer, nullable=False)
    coverage_type = Column(Integer, nullable=False)


class GeoLayerinfo(Base):
    __tablename__ = 'geo_layerinfo'

    id = Column(Integer, primary_key=True)
    work_space = Column(VARCHAR(50), nullable=False)
    title = Column(VARCHAR(100), nullable=False)
    store_name = Column(VARCHAR(100), nullable=False)
    layer_name = Column(VARCHAR(50), nullable=False)
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"))
    is_del = Column(TINYINT(1), nullable=False, server_default=text("'0'"))


class GeoStoreinfo(Base):
    __tablename__ = 'geo_storeinfo'

    id = Column(Integer, primary_key=True)
    work_space = Column(VARCHAR(50), nullable=False)
    store_name = Column(VARCHAR(100), nullable=False)
    store_type = Column(Integer, nullable=False)
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"))
    is_del = Column(TINYINT(1), nullable=False, server_default=text("'0'"))


class GeoWorkspaceinfo(Base):
    __tablename__ = 'geo_workspaceinfo'

    id = Column(Integer, primary_key=True)
    work_space = Column(VARCHAR(50), nullable=False)
    work_space_url = Column(VARCHAR(100), nullable=False)
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"))
    is_del = Column(TINYINT(1), nullable=False, server_default=text("'0'"))


class UserTaskinfo(Base):
    __tablename__ = 'user_taskinfo'

    root_path = Column(VARCHAR(100), nullable=False)
    case_path = Column(VARCHAR(100), nullable=False)
    create_date = Column(DATETIME(fsp=6))
    forecast_date = Column(Date, nullable=False)
    ext = Column(VARCHAR(20), nullable=False)
    id = Column(Integer, primary_key=True)
    state = Column(Integer, nullable=False)
    coverage_area = Column(Integer, nullable=False)
    coverage_type = Column(Integer, nullable=False)


class RelaGeoBase(Base):
    __tablename__ = 'rela_geo_base'

    id = Column(Integer, primary_key=True)
    layer_id = Column(ForeignKey('geo_layerinfo.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    store_id = Column(ForeignKey('geo_storeinfo.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    ws_id = Column(ForeignKey('geo_workspaceinfo.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    task_id = Column(ForeignKey('user_taskinfo.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    coverage_id = Column(ForeignKey('geo_coverageinfo.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    coverage = relationship('GeoCoverageinfo')
    layer = relationship('GeoLayerinfo')
    store = relationship('GeoStoreinfo')
    task = relationship('UserTaskinfo')
    ws = relationship('GeoWorkspaceinfo')


def main():
    Session_class = sessionmaker(bind=engine)
    session = Session_class()

    file_name = 'bhs_cur_20200413.nc'
    # file_name = 'ind_cur_20200413.nc'
    # file_name = 'nwp_cur_20200413.nc'
    # file_name = 'scs_cur_20200413.nc'
    # file_name = 'nmefc_wrf_2020041300.nc'

    target_dir = r'c:\data\SearchRescueSys\data\download\COMMON\DAILY\2020\4\13'
    # 记录UserTaskinfo状态
    userTaskInfo = UserTaskinfo()
    userTaskInfo.root_path = DOWNLOAD_ROOT
    userTaskInfo.case_path = target_dir[-(len(target_dir)-len(DOWNLOAD_ROOT)-1):]
    userTaskInfo.create_date = local_to_utc(datetime.now())
    file_path = os.path.join(target_dir, file_name)
    ds = nc.Dataset(file_path)
    ds_xr = xar.open_dataset(file_path)
    forecast_date_utc = pd.to_datetime(ds_xr.coords['time'].values[0])
    userTaskInfo.forecast_date = forecast_date_utc
    userTaskInfo.ext = 'nc'
    userTaskInfo.state = 2
    fileCode = file_name.split('_')
    area_code = fileCode[0]
    type_code = fileCode[1]
    if(len(fileCode) > 2):
        if(type_code == 'cur'):
            userTaskInfo.coverage_type = session.query(DictBase).filter_by(type_code='CURRENT').first().code
            userTaskInfo.coverage_area = session.query(DictBase).filter_by(type_code=area_code).first().code
        elif(type_code == 'wrf'):
            userTaskInfo.coverage_type = session.query(DictBase).filter_by(type_code='WIND').first().code
            userTaskInfo.coverage_area = session.query(DictBase).filter_by(type_code='nwp').first().code
        session.add(userTaskInfo)

    # 记录GeoCoverageinfo状态
    geoCoverageinfo = GeoCoverageinfo()
    fileCode = file_name.split('_')
    if (type_code == 'cur'):
        geoCoverageinfo.root_path = GEO_CURRENT_ROOT
    elif (type_code == 'wrf'):
        geoCoverageinfo.root_path = GEO_WIND_ROOT
    geoCoverageinfo.relative_path = os.path.join(str(datetime.now().date().year),
                                str(datetime.now().date().month), str(datetime.now().date().day))
    geoCoverageinfo.file_name = file_name
    file_size = os.path.getsize(os.path.join(target_dir, file_name))
    geoCoverageinfo.file_size = file_size
    geoCoverageinfo.create_date = local_to_utc(datetime.now())

    if (len(fileCode) > 2):
        if (type_code == 'cur'):
            if (('time' in ds.dimensions) and ('lat' in ds.dimensions) and ('lon' in ds.dimensions)):
                dims = 'time,lat,lon'
            else:
                dims = ''
            if (('u' in ds.variables) and ('v' in ds.variables)):
                vars = 'u,v'
            else:
                vars = ''
            geoCoverageinfo.dimessions = dims
            geoCoverageinfo.variables = vars
            geoCoverageinfo.coverage_type = session.query(DictBase).filter_by(type_code='CURRENT').first().code
            geoCoverageinfo.coverage_area = session.query(DictBase).filter_by(type_code=area_code).first().code
        elif (type_code == 'wrf'):
            if(('time' in ds.dimensions) and ('latitude' in ds.dimensions) and ('longitude' in ds.dimensions)):
                dims = 'time,latitude,longitude'
            else:
                dims = ''
            if (('U10' in ds.variables) and ('V10' in ds.variables)):
                vars = 'U10,V10'
            else:
                vars = ''
            geoCoverageinfo.dimessions = dims
            geoCoverageinfo.variables = vars
            geoCoverageinfo.coverage_type = session.query(DictBase).filter_by(type_code='WIND').first().code
            geoCoverageinfo.coverage_area = session.query(DictBase).filter_by(type_code='nwp').first().code
        session.add(geoCoverageinfo)

    # 记录geoStoreinfo状态
    geoStoreinfo = GeoStoreinfo()
    fileCode = file_name.split('_')
    if (type_code == 'cur'):
        geoStoreinfo.work_space = _WORK_SPACE.get('CURRENT')
    elif (type_code == 'wrf'):
        geoStoreinfo.work_space = _WORK_SPACE.get('WIND')
    geoStoreinfo.store_name = file_name[:(len(file_name)-3)]
    geoStoreinfo.store_type = 301
    session.add(geoStoreinfo)

    session.commit()
    pass


if __name__ == '__main__':
    main()
    pass