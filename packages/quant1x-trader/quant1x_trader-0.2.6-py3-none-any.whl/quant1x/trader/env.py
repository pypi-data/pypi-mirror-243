#!/usr/bin/python
# -*- coding: UTF-8 -*-

import getpass
import os
import platform

import win32com.client


def get_quant1x_config_filename() -> str:
    """
    获取quant1x.yaml文件路径
    :return:
    """
    # 默认配置文件名
    default_config_filename = 'quant1x.yaml'
    yaml_filename = '~/runtime/etc/' + default_config_filename
    system = platform.system().lower()
    if system == 'windows':
        user_home = os.getenv("GOX_HOME")
        if len(user_home) > 0:
            user_home = user_home.strip()
        if len(user_home) == 0:
            user_home = '~'
        quant1x_root = user_home + '/' + '.quant1x'
        yaml_filename = os.path.expanduser(quant1x_root + '/' + default_config_filename)
    yaml_filename = os.path.expanduser(yaml_filename)
    return yaml_filename


def get_gjzq_qmt_exec_path() -> str:
    """
    获取QMT安装路径
    """
    username = getpass.getuser()  # 当前用户名
    qmt_exec_lnk = rf'C:\Users\{username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\国金证券QMT交易端\启动国金证券QMT交易端.lnk'
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(qmt_exec_lnk)
    # print(shortcut.Targetpath)
    target_path = str(shortcut.Targetpath)
    paths = target_path.split(r'\bin.x64')
    exec_path = os.path.expanduser(paths[0])
    exec_path = exec_path.replace('\\', '/')
    return exec_path


if __name__ == '__main__':
    path = get_gjzq_qmt_exec_path()
    print(path)
