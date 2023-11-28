#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/13 13:50
# @Author  : streamer
# @File    : loader.py
# @Project : celery_spider
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/11/13   CREATE
import numbers
from operator import itemgetter
from celery.utils.imports import symbol_by_name
from celery.app import backends

loader_by_name = symbol_by_name


def without_none_values(iterable):
    """Return a copy of ``iterable`` with all ``None`` entries removed.

    If ``iterable`` is a mapping, return a dictionary where all pairs that have
    value ``None`` have been removed.
    """
    try:
        return {k: v for k, v in iterable.items() if v is not None}
    except AttributeError:
        return type(iterable)((v for v in iterable if v is not None))


def build_component_list(comp_info, custom=None):
    """Compose a component list from a { class: order } dictionary."""

    if comp_info is None:
        comp_info = {}

    def _validate_values(comp_dict):
        """Fail if a value in the components dict is not a real number or None."""
        for name, value in comp_dict.items():
            if value is not None and not isinstance(value, numbers.Real):
                raise ValueError(
                    f"Invalid value {value} for component {name}, "
                    "please provide a real number or None instead"
                )

    if custom is not None:
        comp_info.update(custom)

    _validate_values(comp_info)
    comp_info = without_none_values(comp_info)
    return [k for k, v in sorted(comp_info.items(), key=itemgetter(1))]


def item_backend_by_url(url=None, app_loader=None):
    # Return item backend by url
    # TODO 应该写在一个专门的文件里边的
    from celery.app import backends
    item_backend_aliases = {
        'mongodb': 'spider.base.easy_item_backend: ItemMongoBackend',
    }
    app_loader = app_loader or backends.current_app.loader_by_name

    # 保存原始的配置
    origin_backend_settings = app_loader.override_backends.copy()
    origin_aliases = backends.BACKEND_ALIASES.copy()
    origin_unknown_item_backend = backends.UNKNOWN_BACKEND

    # 更换成item backend 的配置
    app_loader.override_backends = backends.current_app.conf.get('item_backend', {})
    backends.UNKNOWN_BACKEND = """
Unknown item backend: {0!r}.  Did you spell that correctly? ({1!r})
"""
    backends.BACKEND_ALIASES.update(item_backend_aliases)

    # 通过url 获取item backend
    item_backend, url = backends.by_url(url, loader_by_name)

    # 还原配置
    app_loader.override_backends = origin_backend_settings
    backends.BACKEND_ALIASES = origin_aliases
    backends.UNKNOWN_BACKEND = origin_unknown_item_backend

    return item_backend, url
