# -*- coding: utf-8 -*-
# @project: duspider
# @Author：dyz
# @date：2023/11/9 9:48
import time
from hashlib import md5


def make_md5(s: str, encoding='utf-8') -> str:
    """MD5 加密"""
    return md5(s.lower().encode(encoding)).hexdigest()


def aio_timer(func):
    """ 计算时间装饰器 """

    async def wrapper(*args, **kwargs):
        start_time = time.time()
        res = await func(*args, **kwargs)
        time_ = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
        print(f'总耗时: {time_}')
        return res

    return wrapper
