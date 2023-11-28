#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/12 05:23
# @Author  : streamer
# @File    : easy_item.py
# @Project : e_commerce
# @Software: PyCharm
# @History : 
# VERSION     USER      DATE         DESC
# v1.0.0      Streamer   2023/6/12   CREATE

from abc import ABCMeta
from collections.abc import MutableMapping
from copy import deepcopy
from pprint import pformat
from typing import Dict
from spider.utils.trackref import ObjectRef


class Attr(dict):
    """attribute"""


is_debug = False


def print_info(info):
    if is_debug:
        import pprint
        pprint.pprint(info)


class BaseModelMeta(ABCMeta):

    def __new__(mcs, class_name, bases, attrs):
        classcell = attrs.pop("__classcell__", None)
        new_bases = tuple(base._class for base in bases if hasattr(base, "_class"))
        print_info(f'super() type:{type(super())}, value:{super()}')
        _class = super().__new__(mcs, "x_" + class_name, new_bases, attrs)
        print_info(f'_class type:{type(_class)}, value:{_class}')
        fields = getattr(_class, "fields", {})
        print_info(f'fields type:{type(fields)}, value:{fields}')
        new_attrs = {}
        for n in dir(_class):
            v = getattr(_class, n)
            if isinstance(v, Attr):
                fields[n] = v
            elif n in attrs:
                new_attrs[n] = attrs[n]

        new_attrs["fields"] = fields
        new_attrs["_class"] = _class
        if classcell is not None:
            new_attrs["__classcell__"] = classcell
        return super().__new__(mcs, class_name, bases, new_attrs)


class BaseItem(MutableMapping, ObjectRef, metaclass=BaseModelMeta):
    fields: Dict[str, Attr]

    def __init__(self, *args, **kwargs):
        self._values = {}
        if args or kwargs:  # avoid creating dict for most common case
            for k, v in dict(*args, **kwargs).items():
                self[k] = v

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        self._values[key] = value

    def __delitem__(self, key):
        del self._values[key]

    def __getattr__(self, name):
        if name in self.fields:
            return self.__getitem__(name)
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name in self.fields:
            self.__setitem__(name, value)
        else:
            super().__setattr__(name, value)

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    __hash__ = ObjectRef.__hash__

    def keys(self):
        return self._values.keys()

    def __repr__(self):
        return pformat(dict(self))

    def copy(self):
        return self.__class__(self)

    def deepcopy(self):
        """Return a :func:`~copy.deepcopy` of this item."""
        return deepcopy(self)

    @property
    def id(self):
        if hasattr(self, 'id') or 'id' in self.__dict__.keys():
            return self.__dict__['id']
        elif hasattr(self, '_id') or '_id' in self.__dict__.keys():
            return self.__dict__['_id']
        else:
            # TODO  set my exception
            raise Exception(f'no id field in {self.__class__.__name__}')
