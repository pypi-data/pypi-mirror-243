# -*- coding:utf-8 -*-
# Time:   2023/10/30 1:41
# Author: streamer
# Email:  streamer5538@gmail.com
from .base import MiddlewareManger
from spider.network import Request, Response, download_page
from typing import Any, Callable, Union, cast
from spider.base.easy_chain import PairErrBackChain


class DownloaderMiddlewareManager(MiddlewareManger):
    component_name = 'downloader_middleware'

    def _add_middlewares(self, mw: Any) -> None:
        if hasattr(mw, 'process_request') and callable(mw.process_request):
            self.methods['process_request'].append(mw.process_request)
        if hasattr(mw, 'process_response') and callable(mw.process_response):
            self.methods['process_response'].appendleft(mw.process_response)
        if hasattr(mw, 'process_exception') and callable(mw.process_exception):
            self.methods['process_exception'].appendleft(mw.process_exception)

    def download(self, request: Request, download_func: Callable = None) -> Union[Request, Response, Exception]:
        if download_func is None:
            download_func = download_page

        def process_request(req: Request) -> Union[Request, Response]:

            for method in self.methods['process_request']:
                method = cast(Callable, method)
                resp = method(req)
                if resp is not None and not isinstance(resp, (Response, Request)):
                    # TODO set my value exception
                    raise TypeError(
                        f'Middleware {method.__qualname__} must return Response or Request, '
                        f'got {resp.__class__.__name__}'
                    )
                elif isinstance(resp, Request):
                    req = resp
                else:
                    return resp
            return download_func(request=req)

        def process_response(resp: Response) -> Union[Request, Response]:
            if resp is None:
                raise TypeError(f'Received None in Middleware[{self.component_name}] process_response')
            elif isinstance(resp, Request):
                return resp

            for method in self.methods['process_response']:
                method = cast(Callable, method)
                # FIXME this request never through process_request
                resp = method(request=request, response=resp)
                if not isinstance(resp, (Response, Request)):
                    # TODO set my exception type
                    raise TypeError(
                        f'Middleware {method.__qualname__} must return Response or Request,'
                        f'get {type(resp)}'
                    )
                if isinstance(resp, Request):
                    return resp
            return resp

        def process_exception(ex: Exception) -> Union[Request, Response, Exception]:
            for method in self.methods['process_exception']:
                method = cast(Callable, method)
                resp = method(request=request, exception=ex)
                if resp is not None and not isinstance(resp, (Response, Request)):
                    raise TypeError(
                        f'Middleware {method.__qualname__} must return None, Response or Request,'
                        f'got {type(resp)}'
                    )
                if resp:
                    return resp
            return ex

        download_chain = PairErrBackChain()
        download_chain.add_callback(process_request)
        download_chain.add_callback(process_response)
        download_chain.add_err_callback(process_exception)
        download_chain.callback(request)
        return download_chain.result
