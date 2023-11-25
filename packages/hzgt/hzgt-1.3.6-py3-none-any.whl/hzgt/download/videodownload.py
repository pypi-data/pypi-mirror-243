import os
import subprocess
import time

try:
    from hzgt import restrop
except ImportError as err:
    print("hzgt", "import err... ===>>>", err)
    os.system('pip install hzgt')
    from hzgt import restrop


def VideoDownload(url, savepath="download_Files\\youget"):
    current_path = os.getcwd() + "\\" + savepath
    cmd = f'you-get "{url}" -o "{current_path}"'
    print("cmd命令：", restrop(cmd, f=5))

    screenData = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    current_line: str = ' '
    while True:
        line = screenData.stdout.readline().replace(b"\r\n", b"")
        _line = line.decode().strip("b'")
        print(_line)
        time.sleep(0.017)
        if _line == '' and current_line == _line:  # or subprocess.Popen.poll(screenData) == 0:
            screenData.stdout.close()
            break
        current_line = _line


if __name__ == "__main__":
    url = input('输入视频url地址：')
    VideoDownload(url)
