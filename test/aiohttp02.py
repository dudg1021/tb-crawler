#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: diange.du
@file: aiohttp02.py
@time: 2020/5/25 17:41
@desc: aiohttp 多任务测试
'''

import time
import asyncio
import aiohttp
import aiomysql
from utils.config import *
total = 2


async def request(item, pool):
    req_context = ''
    while True:
        startTime = time.time()
        await asyncio.sleep(1)
        url = f'http://127.0.0.1:5000/?item={item}&info={req_context}'

        print(f'await before - {item}, 耗时：{time.time() - startTime}')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp_text = await resp.text()
                req_context = resp_text
                print(f'await after 第 {item} 次请求结果：{resp_text}, 耗时：{time.time() - startTime}')
                await request_detail(item,pool)


async def request_detail(item,pool):
    startTime = time.time()
    url = f'http://127.0.0.1:5000/detail?item={item}'
    # print(f'await before - {item}, 耗时：{time.time() - startTime}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp_text = await resp.text()
            sql = "insert into city_tmp(name) values('hello world')"
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(sql)
                    await conn.commit()
            print(f'await after 第 {item} 次请求detail结果：{resp_text}, 耗时：{time.time() - startTime}')


async def main(loop):
    pool = await aiomysql.create_pool(host=MYSQL_URL, port=MYSQL_PORT, user=USER, password=PASSWORD,
                                      db='direct_selling', loop=loop)

    tasks = [asyncio.ensure_future(request(i,pool)) for i in range(0, total)]
    return await asyncio.gather(*tasks)


if __name__ == '__main__':
    time0 = time.time()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    finally:
        loop.close()
    time1 = time.time()
    print("爬取{0}个网页 ，总花费时间:{1:.2f}s".format(
        total, time1 - time0), end="")
