#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/25 10:46
# @Author  : streamer
# @File    : request.py
# @Project : celery_spider
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/10/25   CREATE
from spider.base import EasyObj
from spider.utils import get_full_name


class Request(EasyObj):
    def __init__(self, url=None, callback=None, method='GET', headers=None, data=None, meta=None, **kwargs):
        self.url = url
        self.method = method
        self.headers = headers
        self.data = data
        self.meta = meta
        self.callback = callback
        EasyObj.__init__(self, **kwargs)

    def import_callback(self, module):
        # path = f'{module}.{self.callback}'
        # # module = symbol_by_name(module)
        # # self.callback = getattr(module, self.callback)
        # self.callback = load_function(path)
        # return self
        pass

    @property
    def str_callback(self):
        callback = ''
        if 'callback' in self.__dict__.keys() and callable(self.callback):
            # callback = self.__dict__.pop('callback')
            callback = get_full_name(self.callback)
        return callback

    @property
    def serialize(self):
        data = {
            k: v for k, v in self.__dict__.items()
            if v and (not (k.startswith('_') or callable(getattr(self, k))))
        }
        # if 'callback' in self.__dict__.keys():
        #     del data['callback']
        # data.update({
        #     k: v for k, v in self.__dict__.items()
        #     if v and (not (k.startswith('_') or callable(getattr(self, k))))
        # })
        return data

    @property
    def serialize_with_callback_str(self):
        data = self.serialize
        data['callback'] = self.str_callback
        return data


