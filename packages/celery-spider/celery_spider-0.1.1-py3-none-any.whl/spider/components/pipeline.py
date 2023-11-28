# -*- coding:utf-8 -*-
# Time:   2023/10/30 1:41
# Author: streamer
# Email:  streamer5538@gmail.com
from typing import Any

from .base import MiddlewareManger
from spider.base.easy_chain import SkipOnErrChain


class PipelineMiddlewareManager(MiddlewareManger):
    component_name = 'pipeline_middlewares'

    def _add_middleware(self, pipe: Any) -> None:
        if hasattr(pipe, 'process_item') and callable(pipe.process_item):
            self.methods['process_item'].append(pipe.process_item)

    def process_item(self, item: Any) -> Any:
        # process crawl item
        chain = SkipOnErrChain()
        for method in self.methods['process_item']:
            chain.add_callback(method)

        chain.callback(item)
        return chain.result


