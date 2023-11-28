#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/3 16:14
# @Author  : streamer
# @File    : __init__.py.py
# @Project : celery_spider
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/11/3   CREATE
from typing import Any, List, Union, Callable


def get_full_name(obj: Any) -> str:
    return f'{obj.__module__}.{obj.__qualname__}'


def get_obj_func(
        obj: Any, func_name: str = None, start_with: str = None, end_with: str = None, contains: str = None
) -> List[Union[Callable, None]]:
    if func_name is not None and hasattr(obj, func_name) and callable(getattr(obj, func_name)):
        return [getattr(obj, func_name)]
    if start_with is not None:
        return [getattr(obj, func_name) for func_name in dir(obj) if
                func_name.startswith(start_with) and callable(getattr(obj, func_name))]
    if end_with is not None:
        return [getattr(obj, func_name) for func_name in dir(obj) if
                func_name.endswith(end_with) and callable(getattr(obj, func_name))]
    if contains is not None:
        return [getattr(obj, func_name) for func_name in dir(obj) if
                contains in func_name and callable(getattr(obj, func_name))]
    return []
