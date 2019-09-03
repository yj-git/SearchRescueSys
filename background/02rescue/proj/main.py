import sys
import os
import mongoengine

# ---
# 加载本项目的部分包
from conf import setting
from core import data

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def main():
    dir_path = setting.DIR
    file_name = setting.FILE_NAME
    search = data.SearchRescueData(dir_path, file_name)
    search.init()
    search.insert2DB()
    print('写入完成')
    pass


if __name__ == '__main__':
    main()
