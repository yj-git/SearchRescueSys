import sys
import os
import mongoengine

# ---
# 加载本项目的部分包
from conf import setting
from core import data,common

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def main():
    dir_path = setting.DIR
    file_name = setting.FILE_NAME

    # search = data.SearchRescueData(dir_path, file_name)
    # search.init()
    # search.insert2DB()
    # TODO:[*] 19-09-18 将上面的方式进行解耦，写成工厂方法

    data_factory= data.DataFactory(common.DataType.Oil_Spilling)
    data_factory.run(dir_path, file_name)

    print('写入完成')
    pass


if __name__ == '__main__':
    main()
