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

from .components import (
    MiddlewareManger,
    DownloaderMiddlewareManager,
    SpiderParserManager,
    PipelineMiddlewareManager
)
from spider.base.easy_item_backends import ItemMongoBackend
from functools import wraps, update_wrapper, cached_property
from collections.abc import Iterator
from celery import Celery, Task

from .base import BaseItem
from spider.network import Request
from spider.utils.loader import loader_by_name, item_backend_by_url
import logging

from .utils import get_full_name

logger = logging.getLogger(__name__)


class CeleryMixin(Celery):

    def __init__(self, main=None, loader=None, backend=None, amqp=None, events=None, log=None, control=None,
                 set_as_current=True, tasks=None, broker=None, include=None, changes=None, config_source=None,
                 fixups=None, task_cls=None, autofinalize=True, namespace=None, strict_typing=True, **kwargs):
        super().__init__(main, loader, backend, amqp, events, log, control, set_as_current, tasks, broker, include,
                         changes, config_source, fixups, task_cls, autofinalize, namespace, strict_typing, **kwargs)


class SpiderMixin:
    downloader_cls = 'spider.components.downloader.DownloaderMiddlewareManager'
    parser_cls = 'spider.components.parser.SpiderParserManager'
    pipeline_cls = 'spider.components.pipeline.PipelineMiddlewareManager'
    item_backend_cls = None

    # downloader: DownloaderMiddlewareManager = None
    # parser: SpiderParserManager = None
    # pipeline: PipelineMiddlewareManager = None

    def __init__(self, name=None, *, downloader_cls=None, parser_cls=None, pipeline_cls=None,
                 item_backend_cls=None, **kwargs):
        self.spider_name = name or self.__class__.__name__
        # super().__init__(name, **kwargs)
        self.downloader_cls = downloader_cls or self.downloader_cls
        self.parser_cls = parser_cls or self.parser_cls
        self.pipeline_cls = pipeline_cls or self.pipeline_cls
        self.item_backend_cls = item_backend_cls or self.item_backend_cls

        self._item_backend_cached = None

    @cached_property
    def downloader(self) -> DownloaderMiddlewareManager:
        return self._init_downloader()

    @cached_property
    def parser(self) -> SpiderParserManager:
        return self._init_parser()

    @cached_property
    def pipeline(self) -> PipelineMiddlewareManager:
        return self._init_pipeline()

    def _init_downloader(self):
        downloader_cls = loader_by_name(self.downloader_cls)
        return downloader_cls.from_settings(self.conf)

    def _init_parser(self):
        parser_cls = loader_by_name(self.parser_cls)
        parser = parser_cls.from_settings(self.conf, self)
        # self.load_task_from_parser(parser)
        return parser

    def _init_pipeline(self):
        pipeline_cls = loader_by_name(self.pipeline_cls)
        return pipeline_cls.from_settings(self.conf)

    def _crawl_flow(self, parse_func):
        """spider crawl flow"""

        @wraps(parse_func)
        # TODO HACK should make crawl args and kwargs to Request class
        def crawl(url, *args, **kwargs):

            result = {}
            items = []
            request = Request(url, *args, **kwargs)
            # TODO Add Features: Custom download methods can be loaded from settings
            resp = self.downloader.download(request=request, download_func=None)

            # TODO Add Features: Choose whether to parse web pages in this node from settings
            parse_result = parse_func(resp)

            # sure parser_result is generator
            if not (hasattr(parse_result, '__next__') and callable(getattr(parse_result, '__next__'))):
                if isinstance(parse_result, Iterator):
                    parse_result = (x for x in parse_result)
                else:
                    parse_result = (x for x in [parse_result])
            is_continued = True
            while is_continued:
                try:
                    item = next(parse_result)
                except StopIteration as e:
                    item = e.value  # make sure can get item when use return in parse_func
                    is_continued = False

                if isinstance(item, Request):
                    self.publish_crawl_task(item)
                # elif isinstance(item, Task):  # 貌似不会yield Task 的情况出现

                elif isinstance(item, BaseItem):
                    item = self.pipeline.process_item(item)
                    # TODO 添加可以根据settings或者opts 自动设定存储item的功能
                    item = self.store_item(item)
                    items.append(item)
                else:
                    # TODO setting my exception
                    logger.warning(f'methods[{parse_func.__qualname__}] should yield or return Request or Item'
                                   f', got %s' % type(item))

            # TODO 丰富日志的打印
            logger.info(f'crawl {len(items)} items in page[url="{url}"]')

            result['item_ids'] = [item.id for item in items]

            return result

        return crawl

    def crawl_task(self, *args, **kwargs):
        def wrapper(func):

            _crawl_flow = self._crawl_flow(func)
            new_args = (_crawl_flow,) + args[1:]
            update_wrapper(_crawl_flow, func)

            task = self.task(*new_args, **kwargs)

            return task

        if len(args) == 1 and callable(args[0]):
            return wrapper(args[0])
        else:
            return wrapper

    def _init_base_crawl_task(self):
        def _base_task(*args, **kwargs):
            request = Request(*args, **kwargs)
            parse_func_name = request.callback
            if parse_func := self.parser.get_thread_safe(parse_func_name):
                return self._crawl_flow(parse_func)(*args, **kwargs)
            else:
                # TODO  set my exception
                raise Exception(f'parse_func[{parse_func_name}] not found')

        task = self.task(_base_task, name='base_crawl')
        return task

    def publish_crawl_task(self, request: Request) -> None:
        # TODO 根据settings 在这里添加去重逻辑
        crawl_task = self.tasks.get(request.str_callback)
        if crawl_task is not None:
            crawl_task.delay(**request.serialize)
        else:
            self.parser.contains_parser(request.callback)
            crawl_task = self.base_crawl_task
            crawl_task.delay(**request.serialize_with_callback_str)

    def task(self, *args, **opts) -> Task:
        """celery class task"""

    @cached_property
    def base_crawl_task(self):
        if task := self.tasks.get('base_crawl'):
            return task
        else:
            # TODO Set my exception
            raise Exception('base_crawl task not found')

    def store_item(self, item):
        raise NotImplementedError

    @property
    def conf(self):
        """celery class conf"""
        raise NotImplementedError

    @property
    def tasks(self):
        """celery class tasks"""
        raise NotImplementedError


class CelerySpider(CeleryMixin, SpiderMixin):
    item_backend_cls = None

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    @property
    def _item_backend(self):
        if self._item_backend_cached is not None:
            return self._item_backend_cached
        return getattr(self._local, 'item_backend', None)

    @_item_backend.setter
    def _item_backend(self, item_backend):
        if item_backend.thread_safe:
            self._item_backend_cached = item_backend
        else:
            self._local.backend = item_backend

    @property
    def item_backend(self):
        if self._item_backend is None:
            self._item_backend = self._get_item_backend()
        return self._item_backend

    def _get_item_backend(self):
        # TODO 设置一个参数, 确定是否result 和item 是否使用同一个数据库,这样可以减少数据库的连接参数设置
        if self.conf.get('item_use_result_backend', True):
            self.conf.item_backend = self.conf.result_backend
        backend, url = item_backend_by_url(
            self.item_backend_cls or self.conf.item_backend,
            self.loader
        )
        return backend(app=self, url=url)

    def store_item(self, item):
        return self.item_backend.store_item(item)

    # def on_init(self):
    #     self._init_base_crawl_task()

    # def start(self, argv=None):
    #     self.parser.update_settings(self.conf)
    #     self._init_base_crawl_task()
    #     super().start(argv=argv)

    def worker_main(self, argv=None):
        self.parser.update_settings(self.conf)
        self._init_base_crawl_task()
        super().worker_main(argv=argv)
