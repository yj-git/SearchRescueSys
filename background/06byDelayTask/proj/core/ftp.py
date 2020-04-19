#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 16:55
# @Author  : evaseemefly
# @Desc    : ftp工具类，用来根据传入的 file 类型，获取匹配的 file names
# @Site    : 
# @File    : ftp.py
# @Software: PyCharm
import os
from ftplib import FTP, FTP_TLS
from ftplib import error_perm
import socket
from fnmatch import fnmatch, fnmatchcase

from typing import List

# 当前项目
from core.file import ICoverageFile, IFileBase
from core.db import DbFile
from util.tools import check_path_exist, exe_run_time
from conf.settings import _MYSQL

# 日志
from common.exceptionLog import exception
from common.log import logger


class FtpFactory:
    def __init__(self, host, user, pwd, port=21):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.ftp: FTP = None

    def init_ftp(self):
        '''
            初始化ftp
        :return:
        '''
        if self.ftp is None:
            self.ftp = FTP()
            if all([self.host, self.user, self.pwd]):
                # 参考
                try:
                    self.ftp.set_debuglevel(0)
                    self.ftp.connect(self.host, self.port)
                    self.ftp.login(self.user, self.pwd)
                    print(self.ftp.getwelcome())
                    # msg=self.ftp.retrlines('LIST xb*')
                except(socket.error, socket.gaierror):
                    print(f"连接错误:{self.host, self.port}")
                    self.ftp = None
                except error_perm:
                    # 认证错误
                    print("认证错误，请检查用户名及密码")
                    self.ftp = None
                except Exception as e:
                    print(f"其他未知错误{e}")
                    self.ftp = None

    def get_all_list(self) -> List[str]:
        '''
            获取当前路径下的全部文件
        :return:
        '''
        return self.ftp.nlst()

    def _get_match_list(self, file: IFileBase) -> List[str]:
        list_all_names = self.get_all_list()
        list_match_names = [name for name in list_all_names if fnmatch(name, file.get_re)]
        return list_match_names

    def _download_file(self, file_name: str, local_path: str):
        '''
            将ftp目录下的指定文件下载至本地的指定目录下
        :param remote_path:
        :param local_path:
        :return:
        '''
        cache_size = 1024

        # 将此方法统一放在common.tools中
        check_path_exist(local_path)
        print(f"开始下载{file_name}....")
        fp = open(os.path.join(local_path, file_name), 'wb')
        # 读取指定文件并写入本地文件
        # 错误1:ftplib.error_perm: 500 Syntax error, command unrecognized.
        msg = self.ftp.retrbinary('RETR ' + file_name, fp.write, cache_size)
        # 判断ftp返回的状态
        if msg.find('226') != -1:
            print(f"{file_name}下载完毕,存储至:{os.path.join(local_path, file_name)}")
        self.ftp.set_debuglevel(0)
        fp.close()

    # @exe_run_time()
    @exception(logger)
    def batch_download(self, file: IFileBase):
        '''
            批量下载
            由于定时任务执行时是找到日期去下载当日的全部 栅格 数据，所以只需根据传入的 栅格 file 实现类获取其中的关键信息即可
        @param file:
        @return:
        '''
        if self.ftp is None:
            self.init_ftp()
        if isinstance(file, IFileBase):
            # if file in isinstance(IFileBase):
            # 1 获取正则匹配的 files names
            list_match: List[str] = self._get_match_list(file)
            for file_temp_name in list_match:
                self.download(file_temp_name, file.save_path)

    # @exe_run_time()
    def download(self, file_name: str, target_dir: str):
        '''
            下载单一的文件
        @param file_name: 文件名称
        @param target_dir:下载到的路径
        @return:
        '''
        # 2 执行下载操作,并进行分类存储
        self._download_file(file_name, target_dir)
        # 3 TODO:[*] 20-04-04 下载结束后写入数据库+日志记录 (by cwb)
        db_file = DbFile(_MYSQL.get('HOST'), _MYSQL.get('DB_NAME'), _MYSQL.get('USER'), _MYSQL.get('PASSWORD'))
        db_file.record_state(file_name, target_dir)
        # 4 需要执行标准化操作(by yyq)
        # 5 TODO:[*] 20-04-04 将标准化后的文件信息 写入数据库+日志记录 (by cwb)
