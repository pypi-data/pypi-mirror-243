#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/25 10:56
# @Author  : streamer
# @File    : easy_obj.py
# @Project : celery_spider
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/10/25   CREATE
# TODO 现在暂时没时间完善下载器和下载中间件，所以简单写个obj和dict 可以相互转换的类
class EasyObj:
    """
    简单的对象类型, 用于存储简单的对象信息
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return vars(self).copy()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'

    def __str__(self):
        return f'{self.__class__.__name__}({self.__dict__})'


