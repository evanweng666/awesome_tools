import requests

"""
@Title  requests工具
@Author Evan
"""


def default_get_proxy():
    """
    默认获取代理IP函数
    :return:
    """
    pass


def default_delete_proxy(proxy):
    """
    默认删除代理IP函数
    :return:
    """
    pass


def get(url, retry_count=5, params=None, **kwargs):
    """
    GET请求
    :param url: 请求地址
    :param retry_count: 重试次数
    :param params: 请求参数
    :param kwargs: 其他参数
    :return:
    """
    for i in range(retry_count):
        try:
            res = requests.get(url, params=params, timeout=5, **kwargs)
            return res
        except BaseException as e:
            print('get req error, url = [%s], req_count = [%s],  msg = [%s]' % (url, i + 1, str(e)))
    return None


def post(url, retry_count=5, data=None, json=None, **kwargs):
    """
    POST请求
    :param url: 请求地址
    :param retry_count: 重试次数
    :param data: form参数
    :param json: json参数
    :param kwargs: 其他参数
    :return:
    """
    for i in range(retry_count):
        try:
            res = requests.post(url, data=data, json=json, timeout=5, **kwargs)
            return res
        except BaseException as e:
            print('post req error, url = [%s], req_count = [%s],  msg = [%s]' % (url,  i + 1, str(e)))
    return None


def proxy_get(url, retry_count=5, get_proxy=default_get_proxy, delete_proxy=default_delete_proxy, params=None, **kwargs):
    """
    GET代理请求
    :param url: 请求地址
    :param retry_count: 重试次数
    :param get_proxy: 获取代理IP函数
    :param delete_proxy: 删除代理IP函数
    :param params: 请求参数
    :param kwargs: 其他参数
    :return:
    """
    for i in range(retry_count):
        proxy = None
        try:
            proxy = get_proxy()
            if not proxy:
                raise RuntimeError('There is no proxy.')

            res = requests.get(url, proxies={'http': 'http://{}'.format(proxy)}, params=params, timeout=5, **kwargs)
            return res
        except BaseException as e:
            print('proxy get req error, url = [%s], proxy = [%s], req_count = [%s],  msg = [%s]' % (url, proxy, i + 1, str(e)))
            if proxy:
                try:
                    delete_proxy(proxy)
                except BaseException as de:
                    print('delete proxy error, proxy = [%s], msg = [%s]' % (proxy, str(de)))
    return None


def proxy_post(url, retry_count=5, get_proxy=default_get_proxy, delete_proxy=default_delete_proxy, data=None, json=None, **kwargs):
    """
    POST代理请求
    :param url: 请求地址
    :param retry_count: 重试次数
    :param get_proxy: 获取代理IP函数
    :param delete_proxy: 删除代理IP函数
    :param data: from参数
    :param data: json
    :param kwargs: 其他参数
    :return:
    """
    for i in range(retry_count):
        proxy = None
        try:
            proxy = get_proxy()
            if not proxy:
                raise RuntimeError('There is no proxy.')
            res = requests.post(url, proxies={'http': 'http://{}'.format(proxy)}, data=data, json=json, timeout=5, **kwargs)
            return res
        except BaseException as e:
            print('proxy post req error, url = [%s], proxy = [%s], req_count = [%s],  msg = [%s]' % (url, proxy, i + 1, str(e)))
            if proxy:
                try:
                    delete_proxy(proxy)
                except BaseException as de:
                    print('delete proxy error, proxy = [%s], msg = [%s]' % (proxy, str(de)))
    return None
