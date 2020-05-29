#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: diange.du
@file: aiohttp03.py
@time: 2020/5/26 14:08
@desc:
'''
import re
import time
import asyncio
import aiohttp
total = 2


async def request(item):
    while True:
        startTime = time.time()
        await asyncio.sleep(6)
        url = 'https://login.taobao.com/member/login.jhtml'

        print(f'await before - {item}, 耗时：{time.time() - startTime}')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp_text = await resp.text()
                umidEncryptAppName = re.findall(r'"umidEncryptAppName":(.+?),', resp_text)[0].strip('"')
                print(umidEncryptAppName)
                print(f'await after 第 {item} 次请求结果：{resp_text}, 耗时：{time.time() - startTime}')
                await request_detail(item)


async def request_detail(item):
    startTime = time.time()
    url = f'http://127.0.0.1:5000/detail?item={item}'
    # print(f'await before - {item}, 耗时：{time.time() - startTime}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp_text = await resp.text()
            print(f'await after 第 {item} 次请求detail结果：{resp_text}, 耗时：{time.time() - startTime}')



if __name__ == '__main__':
    time0 = time.time()
    tasks = [asyncio.ensure_future(request(i)) for i in range(0, total)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    time1 = time.time()
    print("爬取{0}个网页 ，总花费时间:{1:.2f}s".format(
        total, time1-time0), end="")