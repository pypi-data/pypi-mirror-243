# -*- coding:utf-8 -*-
# Time:   2023/10/30 1:44
# Author: streamer
# Email:  streamer5538@gmail.com

from .base import ComponentManger
from typing import Any, Dict, Union, Callable
from celery import Task
import threading
from spider.utils import get_full_name, get_obj_func
import logging

logger = logging.getLogger(__name__)
"""
将spider_parser 分解成两个类:
    A、parser_class 保存解析方法和加载解析方法
    B、parser_bridge 维护parser 和spider 的关系，包括保存task-callback, register_crawl，以及在register task 时保存到callback_str
    C、目的： 
        --根据callback 取出task 进行运行， 如果没有task，取出base_task作为task 运行  --> 需要一个字典以callback 为键，task 为值保存关系，命名为parse_task_map
        --需要根据callback_str 取出对应的callback，让base_task 可以实例化进行        --> 需要一个字典以callback_str 为键，callback 为值保存关系, 命名为parsers
        --现在有两种情况; 
            第一种是celery 初始化前加载的parser_callback 都要生成唯一对应的task，方便直接通过task.delay 的调用；
            第二种是动态加载的parser_callback，由于这时候celery 无法注册task了，所以需要在parsers字典中保存信息，方便base_task 加载parse_callback;
                --如何应对这种情况呢：
                    1、最顶级的方法我认为应该修改celery 的task 注册机制，让celery 在运行中也可以注册task；好处是不需要多维护一个parsers 的字典; 
                坏处是需要修改到celery 中的源码，且可能引发线程问题或者不知名问题
                    2、使用双字典进行数据的保存---- celery 中有registry 用来保存task, 只需要将函数的名称替换成full_name就行了（从解析器里边加载的parse 不会定义名字，
                不用担心重载）；只需要维护一个callback_str 的字典就可以了,可以通过callback 来获取名称
        
"""


class SpiderParserManager(ComponentManger):
    """

    parser middleware manager and maintenance relationship between parser and task
    """
    component_name = 'spider_parser'

    def __init__(self, components, spider) -> None:
        self.parsers: Dict[str, Callable] = dict()
        super().__init__(components, spider=spider)
        self.lock = threading.Lock()
        self.task_maker = spider.task
        for cp_name, cp_obj in components.items():
            # print(f'init: component:{cp_obj}, name:{cp_name}')
            self.add_parse_func(cp_obj)

    def set(self, parser_func: Callable, name: str) -> None:
        self.parsers[name] = parser_func

    def get(self, name: str, default) -> Union[Callable, None]:
        return self.parsers.get(name, default)

    def delete(self, name: str) -> None:
        del self.parsers[name]

    def get_thread_safe(self, name: str, default=None) -> Union[Callable, None]:
        with self.lock:
            return self.get(name, default)

    def contains_parser(self, parser: Union[str, Callable]) -> bool:
        """check if parser in parsers, other set parser in parsers"""
        with self.lock:
            if parser in self.parsers.keys():
                return True
            else:
                self.set(parser, parser)
                return False

    def add_parse_func(self, parser_obj: Any) -> None:
        # FIXME 这边需要对parse 做严格的数据限定,不然多线程运行时, spider 类的数据出错
        # TODO 应该设置可以从配置中读取对应的parser, 由于项目需要, 暂时设定从spider类中读取
        parse_funcs = get_obj_func(parser_obj, start_with='parse')
        for parse_func in parse_funcs:
            parse_func_name = get_full_name(parse_func)
            self.set(parse_func, parse_func_name)
            self.task_maker(parse_func, name=parse_func_name)

    def update_settings(self, settings):
        """可能出现在初始化之后 parser_manager 后在加载配置的情况，所以要添加一个更新的方法"""
        new_components = self.load_components(settings)
        for component in new_components:
            if component is not None and component not in self.components:
                self.components[component] = component
                self.add_parse_func(component)

    @classmethod
    def _get_components_from_settings(cls, settings):
        return settings.get(cls.component_name) or settings.get(cls.component_name.upper()) or []

    @classmethod
    def from_settings(cls, settings, spider=None, **kwargs):
        components = cls.load_components(settings)
        return cls(components, spider=spider)
