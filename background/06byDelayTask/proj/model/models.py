from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, text
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey,Sequence,MetaData,Table
from sqlalchemy.orm import relationship,sessionmaker

from datetime import datetime
from conf.settings import DOWNLOAD_ROOT
from common.enum import DownState

engine = create_engine("mysql+pymysql://root:123456@localhost/searchrescue", encoding='utf-8', echo=True)

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
    Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
    # session 会话
    session = Session_class()
#    userTaskInfo = session.query(UserTaskinfo).filter_by(id=1).first()
#    geo = session.query(GeoCoverageinfo).filter_by(id=1).first()
#    code = session.query(DictBase).filter_by(type_code='bhs').first()

    file_name = 'bhs_cur_20200414.nc'
    target_dir = r'C:\data\SearchRescueSys\data\download\COMMON\DAILY\2020\4\14'
    userTaskInfo = UserTaskinfo()
    userTaskInfo.root_path = DOWNLOAD_ROOT
    userTaskInfo.case_path = target_dir
    userTaskInfo.create_date = datetime.now()
    userTaskInfo.forecast_date = datetime.now().date()
    userTaskInfo.ext = 'nc'
    #userTaskInfo.id = Column(Integer, primary_key=True)
    #userTaskInfo.state = DownState.COMPLETED
    userTaskInfo.state = 2

    fileCode = file_name.split('_')
    if(len(fileCode) > 2):
        userTaskInfo.coverage_area = session.query(DictBase).filter_by(type_code=fileCode[0]).first().code
        if(fileCode[1] == 'cur'):
            userTaskInfo.coverage_type = session.query(DictBase).filter_by(type_code='CURRENT').first().code
            session.add(userTaskInfo)
            session.commit()
    pass


if __name__ == '__main__':
    main()
    pass