# coding=utf-8
from __future__ import print_function, absolute_import
from datetime import datetime
import random
from gm.api import *

_gm_libs_logs = ""


# 日志输出且保存
def log_all(level: str, info: str, source: str = ""):
    log(level=level, msg=info, source=source)
    text = "【{}】 {}".format(level, info)
    print(text)
    append(text)


# 日志不输出仅保存
def log_save(level: str, info: str, source: str = ""):
    log(level=level, msg=info, source=source)
    text = "【{}】 {}".format(level, info)
    append(text)


# 追加信息到日志文件
def append(text: str):
    global _gm_libs_logs
    if _gm_libs_logs == "":
        hash_name = random.getrandbits(128)
        _gm_libs_logs = datetime.today().strftime('%Y-%m-%d') + "%032x" % hash_name
        log_file = open(r"C:\Users\Public\gm_libs_{}.log".format(_gm_libs_logs), "w+", encoding="utf-8")
    else:
        log_file = open(r"C:\Users\Public\gm_libs_{}.log".format(_gm_libs_logs), "a", encoding="utf-8")

    log_file.writelines("{}\n".format(text))
    log_file.close()
