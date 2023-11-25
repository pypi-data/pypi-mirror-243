import datetime
import time

from .strop import restrop, restrop_list

def gettime(func):
    """
    使用方法：装饰器

    在需要显示运算时间的函数前加@gettime

    :param func:
    :return: None
    """
    def get():
        start = datetime.datetime.now()
        print(restrop("==="))
        func()
        end = datetime.datetime.now()
        TotalTimeSpent = (end - start).seconds
        print(restrop_list(["===",
                            "开始时间 ", start.strftime('%Y-%m-%d  %H:%M:%S'),
                            "     结束时间 ", end.strftime('%Y-%m-%d  %H:%M:%S'),
                            "     总耗时 ", TotalTimeSpent, " s"
                            ],
                           [1,
                            -1, 3,
                            -1, 4,
                            -1, 5, -1
                            ])
              )
    return get
