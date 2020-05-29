#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: diange.du
@file: flask01.py
@time: 2020/5/25 16:24
@desc:
'''


from flask import Flask, request
import time

app = Flask(__name__)


@app.route('/')
def index():
    args_item = request.args.get('item')
    args_info = request.args.get('info')
    time.sleep(3)
    return 'hello world - item:{},info:{}'.format(str(args_item), args_info)


@app.route('/detail')
def detail():
    args_item = request.args.get('item')
    time.sleep(2)
    return 'detail - item:{}'.format(str(args_item))


if __name__ == '__main__':
    app.run(threaded=True)