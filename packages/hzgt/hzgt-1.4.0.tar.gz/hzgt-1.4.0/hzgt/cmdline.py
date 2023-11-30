import os
import sys
import locale
import subprocess
import time


def CmdLine(cmd: str, DEFAULTENCODING=''):
    """
    执行cmd命令时可以查看输出的内容
    :param cmd: str 命令
    :param DEFAULTENCODING: str 编码
    """
    if DEFAULTENCODING=='':
        DEFAULTENCODING = str(locale.getpreferredencoding())  # 获取当前环境的默认编码

    screenData = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    current_line: str = ' '
    while True:
        line = screenData.stdout.readline().replace(b"\r\n", b"")
        _line = line.decode(DEFAULTENCODING).strip("b'")
        print(_line)
        time.sleep(0.017)
        if _line == '' and current_line == _line:  # or subprocess.Popen.poll(screenData) == 0:
            screenData.stdout.close()
            break
        current_line = _line
