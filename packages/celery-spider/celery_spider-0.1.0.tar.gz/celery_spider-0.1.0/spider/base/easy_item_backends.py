#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/9 15:48
# @Author  : streamer
# @File    : easy_item_backends.py
# @Project : celery_spider
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/11/9   CREATE
import threading
import time
from datetime import datetime
import pytz
from bson import ObjectId

from celery.exceptions import BackendStoreError
from celery.utils.serialization import raise_with_context
from celery.utils.time import get_exponential_backoff_interval
from spider.utils.trackref import get_create_time
from celery.backends.mongodb import MongoBackend


class TrimBackendMeta(type):
    # TODO 从celery.backends.mongodb import MongoBackend 修剪成base backend，然后删除不需要的代码

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)

        # 删除从mongodb 继承的多余属性
        trim_attrs = [
            'taskmeta_collection',
            'groupmeta_collection',
            '_store_result',
            '_get_task_meta_for',
            '_save_group',

            '_restore_group',
            '_delete_group',
            '_forget',
            'cleanup',
            'collection',
            'group_collection'
        ]
        for attr in trim_attrs:
            if hasattr(instance, attr):
                try:
                    delattr(instance, attr)
                except AttributeError:
                    at = getattr(instance, attr)
                    del at

        return instance


class ItemMongoBackend(MongoBackend, metaclass=TrimBackendMeta):

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        # TODO 读取 settings 中添加 item -> collection 映射的配置
        # TODO 最好添加一个锁，防止多线程同时修改，
        self.collections = {}

    def _get_collection(self, col_name: str):
        # if col_name not in self.collections:
        #     self.collections[col_name] = self.database[col_name]
        # return self.collections[col_name]
        return self.database[col_name]

    def _get_item_meta(self, item):
        # TODO make mongodb ObjectId from obj to str
        obj_id = ObjectId()
        item['_id'] = str(obj_id)
        item_meta = dict(item)
        # TODO 最好在基类里边自动设置item 的create_time, update_time等 追踪时间
        # TODO 可以从settings 中读取 时区
        time_zone = pytz.timezone('Asia/Shanghai')

        item_meta['update_time'] = datetime.now(time_zone)
        create_time_stamp = get_create_time(item)
        utc_time = datetime.utcfromtimestamp(create_time_stamp)
        item_meta['create_time'] = utc_time.replace(tzinfo=pytz.utc).astimezone(time_zone)
        return item_meta

    def get_col(self, name):
        return self._get_collection(name)

    def _store_item(self, item):
        col_name = item.__class__.__name__
        item_meta = self._get_item_meta(item)
        col = self._get_collection(col_name)
        col.insert_one(item_meta)
        return item_meta

    def store_item(self, item):

        retries = 0
        while True:
            try:
                item_meta = self._store_item(item)
                return item_meta
            except Exception as exc:
                if self.always_retry and self.exception_safe_to_retry(exc):
                    if retries < self.max_retries:
                        retries += 1

                        # get_exponential_backoff_interval computes integers
                        # and time.sleep accept floats for sub second sleep
                        sleep_amount = get_exponential_backoff_interval(
                            self.base_sleep_between_retries_ms, retries,
                            self.max_sleep_between_retries_ms, True) / 1000
                        self._sleep(sleep_amount)
                    else:
                        raise_with_context(
                            BackendStoreError("failed to store result on the backend", ),
                        )
                else:
                    raise
