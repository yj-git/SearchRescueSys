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
from util.tools import check_path_exist


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
        fp = open(os.path.join(local_path, file_name), 'wb')
        # 读取指定文件并写入本地文件
        # 错误1:ftplib.error_perm: 500 Syntax error, command unrecognized.
        msg = self.ftp.retrbinary('RETR ' + file_name, fp.write, cache_size)
        # 判断ftp返回的状态
        if msg.find('226') != -1:
            print("下载完毕")
        self.ftp.set_debuglevel(0)
        fp.close()


    def download(self, file: IFileBase):
        # 1 获取正则匹配的 files names
        list_match: List[str] = self._get_match_list(file)
        # 2 执行下载操作
        self._download_file(file.file_name, file.path_dir)
        # 3 下载结束后写入数据库
