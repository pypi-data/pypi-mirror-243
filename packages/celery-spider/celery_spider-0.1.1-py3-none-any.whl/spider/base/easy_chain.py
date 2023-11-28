#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/30 10:05
# @Author  : streamer
# @File    : easy_chain.py
# @Project : celery_spider
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/10/30   CREATE
from typing import (
    Callable,
    Any,
    cast,
    TypeVar,
    Generic,
    List,
    Tuple
)
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T', bound='BaseChain')


def _execute_callback(func: Callable, *args: Any, **kwargs: Any):
    try:
        result = func(*args, **kwargs)
    # TODO set my exception type
    except Exception as e:
        logger.info('when execute callback {} counter exception: {}'.format(func.__name__, e))
        result = e

    return result


class BaseChain(Generic[T]):
    """spider chain class for callbacks and err_callbacks"""

    def __init__(self) -> None:
        self.callbacks: List[Tuple[Callable, Any, Any]] = list()
        self.err_callbacks: List[Tuple[Callable, Any, Any]] = list()
        self._fired: bool = False
        self._result: Any = None

    def add_callback(self, callback: Callable, *args: Any, **kwargs: Any) -> T:
        if self._fired:
            self._result = callback(self._result, *args, **kwargs)
        else:
            self.callbacks.append((callback, args, kwargs))
        return self

    def add_err_callback(self, err_callback: Callable, *args: Any, **kwargs: Any) -> T:
        if self._fired and isinstance(self._result, Exception):
            self._result = err_callback(self._result, *args, **kwargs)
        else:
            self.err_callbacks.append((err_callback, args, kwargs))
        return self

    def callback(self, *args: Any, **kwargs) -> Any:
        # FIXME 为了允许在启动链式反应时可以进行动态传参,需要先进行一次回调,这样可以防止开始运行时的动态参数和后续函数的动态函数不会相互污染
        # FIXME 在找到更好的处理方式前，暂定处理方式为在callback 中进行第一次的回调
        # FIXME callback func must have value args? need fix

        if self.callbacks:
            func, func_args, func_kwargs = self.callbacks.pop(0)
            args = args + func_args
            kwargs.update(func_kwargs)
            result = _execute_callback(func, *args, **kwargs)
            result = self._fire_callbacks(result)
            self._result = result
            self._fired = True

    def _fire_callbacks(self, result: Any) -> None:
        raise NotImplementedError

    @property
    def result(self) -> Any:
        return self._result


class PairErrBackChain(BaseChain):
    """chain class that each callback has a corresponding err_callback"""

    def _fire_callbacks(self, result: Any) -> None:

        # FIXME HACK 关于错误的处理逻辑：通用处理方式，报错时直接从err_callbacks 出队直接回调
        # FIXME HACK 由于没有对callback 和err back 做强制对应, 可能会导致调用时出现差错
        while self.callbacks or self.err_callbacks:
            if isinstance(result, Exception) and self.err_callbacks:
                err_callback, args, kwargs = self.err_callbacks.pop(0)
                result = err_callback(result, *args, **kwargs)
            elif self.callbacks:
                callback, args, kwargs = self.callbacks.pop(0)
                result = _execute_callback(callback, result, *args, **kwargs)
            else:
                break
        return result


class UnifiedErrBackChain(BaseChain):
    """chain class where all callbacks correspond to the same err_callback"""

    def _fire_callbacks(self, result: Any) -> None:
        # FIXME HACK 没有对err_back 有且只有一个限定, 也没有更换err_back 的方法
        while self.callbacks:
            if isinstance(result, Exception) and self.err_callbacks:
                err_callback, args, kwargs = self.err_callbacks[0]
                result = err_callback(result, *args, **kwargs)
            elif self.callbacks:
                callback, args, kwargs = self.callbacks.pop(0)
                result = _execute_callback(callback, result, *args, **kwargs)
            else:
                break


class SkipOnErrChain(BaseChain):
    """chain class that ignores all exceptions generated from callbacks"""

    def _fire_callbacks(self, result: Any) -> None:
        while self.callbacks:
            callback, args, kwargs = self.callbacks.pop(0)
            try:
                new_args = (result,) + args
                result = callback(*new_args, **kwargs)
            except Exception as e:
                logger.warning(f'when {self.__class__.__name__} executes callback {callback.__name__} '
                               f'counter exception: {e}')

