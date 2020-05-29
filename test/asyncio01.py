#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: diange.du
@file: asyncio01.py
@time: 2020/5/25 14:02
@desc:
'''

import time
import requests
import asyncio

total = 3


async def request(item):
    # while True:
    startTime = time.time()
    await asyncio.sleep(6)
    # print(startTime)
    url = f'http://127.0.0.1:5000/?item={item}'
    future = loop.run_in_executor(None, requests.get, url)
    print(f'await before - {item}, 耗时：{time.time() - startTime}')
    response = await future
    print(f'await after 第 {item} 次请求结果：{response.text}, 耗时：{time.time()-startTime}')


if __name__ == '__main__':
    time0 = time.time()
    tasks = [asyncio.ensure_future(request(i)) for i in range(0, total)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    time1 = time.time()
    print("爬取{0}个网页 ，总花费时间:{1:.2f}s".format(
        total, time1-time0), end="")