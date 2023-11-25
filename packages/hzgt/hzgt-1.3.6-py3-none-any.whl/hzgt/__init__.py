import os
import sys

# 版本
from .version._version import __version__
version = __version__

# 字符串操作
from .strop import getmidse, perr, pic, restrop, restrop_list, reputstr

# 获取文件大小
from .fileop import getdirsize, getFileSize, getUrlFileSize

# 字节单位转换
from .fileop import Bit_Unit_Conversion

# 装饰器 gettime获取函数执行时间
from .Decorator_ import gettime

# 文件/github仓库/视频 下载
from .download.download import downloadmain
