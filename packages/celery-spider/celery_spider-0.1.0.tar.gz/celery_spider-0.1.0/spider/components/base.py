# -*- coding:utf-8 -*-
# Time:   2023/10/30 1:08
# Author: streamer
# Email:  streamer5538@gmail.com
from typing import (
    Any,
    Callable,
    Deque,
    Dict,
    Union,
    Tuple, List
)
from collections import defaultdict, deque, OrderedDict
from spider.utils.loader import loader_by_name, build_component_list
import logging
import pprint

logger = logging.getLogger(__name__)


class ComponentManger(object):
    component_name = "component_manager"

    def __init__(self, components, spider=None) -> None:
        self.components: Dict[str, Any] = components
        self.spider = spider

        self.on_init()

    def on_init(self):
        """ Called when spider is init. """


    @classmethod
    def _get_components_from_settings(cls, settings):
        # print(f'{cls.component_name}: {settings.get(cls.component_name) or settings.get(cls.component_name.upper())}')
        return build_component_list(
            settings.get(cls.component_name) or settings.get(cls.component_name.upper())
        )

    @classmethod
    def load_components(cls, settings) -> Dict[str, Any]:
        cp_path = cls._get_components_from_settings(settings)
        components = OrderedDict()
        enabled = []
        for cls_path in cp_path:
            try:
                cp_cls = loader_by_name(cls_path)
                components[cls_path] = cp_cls
                enabled.append(cls_path)
            # TODO set my config error exception
            except Exception as e:
                logger.warning(e)
        logger.info(
            "Enabled %(componentname)ss:\n%(enabledlist)s",
            {
                "componentname": cls.component_name,
                "enabledlist": pprint.pformat(enabled),
            },
        )
        return components

    @classmethod
    def from_settings(cls, settings, spider=None, **kwargs):
        components = cls.load_components(settings)

        return cls(components, spider=spider)

    def _add_middleware(self, mw: Any) -> None:
        raise NotImplementedError


class MiddlewareManger(ComponentManger):
    component_name = "middleware_manager"

    def __init__(self, middlewares, spider) -> None:
        super().__init__(middlewares, spider)
        self.methods: Dict[
            str, Deque[Union[None, Callable, Tuple[Callable, Callable]]]
        ] = defaultdict(deque)

    def on_init(self):
        for mw in self.components.values():
            self._add_middleware(mw)

    @classmethod
    def from_settings(cls, settings, spider=None, **kwargs):
        return cls(*cls.load_components(settings))
