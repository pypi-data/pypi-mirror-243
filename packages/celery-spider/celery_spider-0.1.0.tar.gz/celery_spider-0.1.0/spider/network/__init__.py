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
from requests import request
from selenium import webdriver
from .request import Request
from .response import Response


def download_page(request: Request):
    pass


def request_page(url, method='GET', headers=None, data=None, *args, **kwargs):
    if headers is None:
        headers = {}
    if data is None:
        data = {}
    return request(method, url, headers=headers, data=data, *args, **kwargs)


def request_page_by_selenium(url):
    # TODO 不要一直打开关闭chromedriver，应该做成chromedriver pool
    # step 1:set chromedriver options
    options = webdriver.ChromeOptions()
    options.add_argument('--lang=en')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('log-level=3')
    options.add_argument('--disable-blink-features=AutomationControlled')  # 谷歌浏览器去掉访问痕迹
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/100.0.4896.127 Safari/537.36")
    options.add_argument("--window-size=1920,1050")  # 专门应对无头浏览器中不能最大化屏幕的方案
    # step 2: init chromedriver
    driver = webdriver.Chrome(
        # executable_path=chromedriver_path,
        options=options
    )
    # step 3: access the specified url address
    driver.get(url)
    # step 4: get the page
    resp = Response()
    resp._content = driver.page_source
    resp.url = driver.current_url
    resp.status_code = 200
    driver.quit()
    return resp


