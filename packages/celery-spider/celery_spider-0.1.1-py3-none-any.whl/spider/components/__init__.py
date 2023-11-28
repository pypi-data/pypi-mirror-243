#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/25 10:40
# @Author  : streamer
# @File    : __init__.py.py
# @Project : celery_spider
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/10/25   CREATE
from .downloader import DownloaderMiddlewareManager
from .pipeline import PipelineMiddlewareManager
from .parser import SpiderParserManager
from .base import MiddlewareManger