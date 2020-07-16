import collections
import threading
import functools


"""
@Title  此工具可动态加载数据队列，每次从队列中获取一条数据，并支持单次加载多次使用（线程安全）
@Author Evan
"""

# 数据队列map
qm = {}


def synchronized(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        with self.lock:
            return func(self, *args, **kwargs)
    return wrapper


class QueueWorker(object):
    def __init__(self, rc):
        self.lock = threading.Lock()
        # 数据队列
        self.__dq = collections.deque()
        # 重复次数
        self.__rc = 1 if rc <= 1 else rc
        # 当前次数
        self.__cc = 1
        # 缓存列表
        self.__tl = []

    @synchronized
    def get_one(self, load_data_func):
        if len(self.__dq) > 0:
            return self.__dq.popleft()
        else:
            if self.__cc < self.__rc and self.__tl:
                data_list = self.__tl
                self.__cc = self.__cc + 1
            else:
                data_list = load_data_func()
                self.__tl = data_list
                self.__cc = 1
            if data_list:
                self.__dq.extend(data_list)
                return self.__dq.popleft()
            else:
                return None


def get_one(quque_key, load_data_func, repeat_count=1):
    """
    从指定队列中获取一条数据
    :param quque_key: 队列名称（可多条队列同时使用，用名称区分）
    :param load_data_func: 队列为空时，加载新数据的函数（已加载数据记得做标识，避免加载重复数据）
    :param repeat_count:每次加载数据重复使用的次数（默认为1，仅第一次传入有效）
    :return:
    """
    if quque_key not in qm:
        qm[quque_key] = QueueWorker(repeat_count)
    return qm[quque_key].get_one(load_data_func)
