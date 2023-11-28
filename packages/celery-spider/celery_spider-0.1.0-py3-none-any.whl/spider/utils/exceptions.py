#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/13 13:54
# @Author  : streamer
# @File    : exceptions.py
# @Project : celery_spider
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/11/13   CREATE


class ScrapyDeprecationWarning(Warning):
    """Warning category for deprecated features, since the default
    DeprecationWarning is silenced on Python 2.7+
    """

    pass


