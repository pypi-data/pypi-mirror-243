import os
import sys

import urllib.request

from .sc import SCError


def Bit_Unit_Conversion(fsize: int):
    """
    字节单位转换
    :param fsize: 大小
    :return: 大小,单位,原大小
    """
    if fsize < 1024:
        return round(fsize, 2), 'Byte', fsize
    else:
        KBX = fsize / 1024
        if KBX < 1024:
            return round(KBX, 2), 'K', fsize
        else:
            MBX = KBX / 1024
            if MBX < 1024:
                return round(MBX, 2), 'M', fsize
            else:
                return round(MBX / 1024, 2), 'G', fsize


def getdirsize(dir: str):
    """
    :param dir:目录或者文件
    :return: 目录或者文件的大小
    """
    size = 0
    if os.path.isdir(dir): # 如果是目录
        for root, dirs, files in os.walk(dir):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    elif  os.path.isfile(dir):  # 如果是文件
        size = os.path.getsize(dir)
    return size


def getFileSize(filePath:str):
    """
    获取目录或文件的总大小
    :param filePath: 目录或者文件
    :return: 例子：(2, 'M', 2048)
    """
    try:
        fsize = getdirsize(filePath)  # 返回的是字节大小
        return Bit_Unit_Conversion(fsize)
    except  Exception as err:
        raise SCError(err)


def getUrlFileSize(url: str):
    """
    获取url上的文件的总大小
    :param url: 网络url
    :return: 例子：(2, 'M', 2048)
    """
    try:
        response = urllib.request.urlopen(url)
        file_size = int(response.headers["Content-Length"])
        return Bit_Unit_Conversion(file_size)
    except Exception as err:
        raise SCError(err)
