#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: diange.du
@file: tblogin_shop.py
@time: 2020/3/30 15:08
@desc: 店铺账号- 模拟淘宝登录、获取登录cookies
'''

import re, json
import requests
from lxml import etree
from utils import logutil
s = requests.Session()
log = logutil.log

class taobaoLogin:

    def __init__(self, username, ua, TPL_password2):
        """
        账号登录对象
        :param username: 用户名
        :param ua: 淘宝的ua参数
        :param TPL_password2: 加密后的密码
        """
        # 登录页地址，用于取loginformdata
        self.login_html_url = 'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fi.taobao.com%2Fmy_taobao.htm%3Fspm%3Da21bo.2017.754894437.3.5af911d9LJ31mV%26pm_id%3D1501036000a02c5c3739'
        # 检测是否需要验证码的URL
        self.user_check_url = 'https://login.taobao.com/newlogin/account/check.do?appName=taobao&fromSite=0'
        # 验证淘宝用户名密码URL
        self.verify_password_url = "https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0"
        # 访问URL
        self.mytaobao_url = 'https://i.taobao.com/my_taobao.htm'

        # 淘宝用户名
        self.username = username
        # 淘宝关键参数，包含用户浏览器等一些信息，很多地方会使用，从浏览器或抓包工具中复制，可重复使用
        self.ua = ua
        # 加密后的密码，从浏览器或抓包工具中复制，可重复使用
        self.TPL_password2 = TPL_password2
        self.header = {}
        self.form_data = {}
        # 请求超时时间
        self.timeout = 20000

    def _init_header_data(self):
        # 初始化header
        self.header = {
            'authority': 'login.taobao.com',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'cache-control': 'no-cache',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'origin': 'https://login.taobao.com',
            'upgrade-Insecure-Requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'content-Type': 'application/x-www-form-urlencoded',
            'referer': 'https://login.taobao.com/member/login.jhtml?from=taobaoindex&f=top&style=&sub=true&redirect_url=https%3A%2F%2Fi.taobao.com%2Fmy_taobao.htm',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-site',
        }

        # 初始化form_data  此处通过动态访问网页获取 会触发环境检测 猜测requests和本地浏览器访问有区别
        login_resp = s.get(self.login_html_url, headers=self.header)
        html = etree.HTML(login_resp.text)
        script_txt = html.xpath('//div[@id="content"]/div[@class="content-layout"]/div[@class="login-box-warp"]/script[3]')[0].text
        form_data_str = '{%s}' % (re.findall(r'"loginFormData":{(.+?)},', script_txt)[0])

        self.form_data = json.loads(form_data_str)
        data2 = {
            'loginId': self.username,
            'umidGetStatusVal': 255,
            'screenPixel': '1920x1080',
            'navlanguage': 'zh-CN',
            'navUserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'navPlatform': 'Win32',
            'sub': 'true',
            'returnUrl': self.mytaobao_url,
            'ua': self.ua
        }

        self.form_data.update(data2)
        print(self.form_data)

        # 激活umidtoken
        initial_url = "https://cf.aliyun.com/nocaptcha/initialize.jsonp?a=CF_APP_TBLogin_PC&t=" + self.form_data['umidToken'] + \
            "&scene=&lang=zh_CN&v=v1.2.17&href=https://login.taobao.com/member/login.jhtml&comm={}&callback=initializeJsonp_05827254062167628"
        initial_resp = s.get(initial_url)
        print(initial_resp.text)
        # self.form_data = {
        #     'loginId': self.username,
        #     'umidGetStatusVal': 255,
        #     'screenPixel': '1920x1080',
        #     'navlanguage': 'zh-CN',
        #     'navUserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        #     'navPlatform': 'Win32',
        #     'sub': 'true',
        #     'appName': 'taobao',
        #     'appEntrance': 'taobao_pc',
        #     '_csrf_token': 'IJQbwcnpEgKnRRf6NWAqn3',
        #     'umidToken': '6a1f32d412458970a8053c4f388efc0e317c5fd9',
        #     'isMobile': 'false',
        #     'lang': 'zh_CN',
        #     'hsiz': '11ff39318673c9a7058c9c6ad329de17',
        #     'from': 'tb',
        #     'style': 'default',
        #     'appkey': '00000000',
        #     'returnUrl': self.mytaobao_url,
        #     'ua': self.ua
        # }

    def _user_check(self):
        """
        检测账号是否需要验证码
        :return:
        """
        try:
            self.header['path'] = '/newlogin/account/check.do?appName=taobao&fromSite=0'
            response = s.post(self.user_check_url, data=self.form_data, headers=self.header,
                              timeout=self.timeout)
            response.raise_for_status()
            log.info(f'检查是否需要验证：{response.text}')
        except Exception as e:
            log.error('检测是否需要验证码请求失败，原因：', exc_info=True)
            raise e
        # eg '{"content":{"data":{"resultCode":100},"status":0,"success":true},"hasError":false}'

    def _verify_password(self):
        self.header['path'] = '/newlogin/login.do?appName=taobao&fromSite=0'

        self.form_data['password2'] = self.TPL_password2
        self.form_data['keepLogin'] = 'false'
        try:
            response = s.post(self.verify_password_url, headers=self.header, data=self.form_data,
                              timeout=self.timeout)
            response.raise_for_status()
            log.info(response.text)
            html = json.loads(response.text)
            # 检测用户信息
            if html['content']['data'].get('iframeRedirect') is not None and html['content']['data'].get('iframeRedirect'):
                resp = s.get(html['content']['data']['iframeRedirectUrl'])
                log.info(resp.text)
                resp.raise_for_status()
                html = json.loads(resp.text)
            elif html['content']['data'].get('redirect') is not None and html['content']['data'].get('redirect'):  # 登录成功跳转
                try:
                    resp = s.get(html['content']['data']['redirectUrl'])
                    resp.raise_for_status()

                    # 提取淘宝昵称
                    nick_name_match = re.search(r'<input id="mtb-nickname" type="hidden" value="(.*?)"/>', resp.text)
                    if nick_name_match:
                        log.info('登录淘宝成功，你的用户名是：{}'.format(nick_name_match.group(1)))
                    else:
                        raise RuntimeError('获取淘宝昵称失败！response：{}'.format(resp.text))

                    # 轮询调用异步url
                    if html['content']['data']['asyncUrls'] is not None:
                        for url in html['content']['data']['asyncUrls']:
                            resp = s.get(html['content']['data']['asyncUrls'][0])
                except Exception as e:
                    log.error('获取我的淘宝页请求失败', exec_info=True)
                    raise e
            else:
                # 跳转到我的淘宝页面
                try:
                    resp = s.get(self.mytaobao_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
                    resp.raise_for_status()
                    print(resp.text)
                except Exception as e:
                    log.error('获取淘宝主页请求失败！原因：', exc_info=True)
                    raise e

        except Exception as e:
            log.error('验证用户名和密码请求失败，原因：', exc_info=True)
            raise e

    def save_cookie(self):
        cookies = ''
        try:
            dict_cookies = requests.utils.dict_from_cookiejar(s.cookies)
            for item in dict_cookies:
                str_cookie = '{0}={1};'
                str_cookie = str_cookie.format(item, dict_cookies[item])
                cookies += str_cookie

            log.info(f'cookies: {cookies}')

        except Exception:
            log.error('save_cookie 出错：', exc_info=True)
        return cookies

    def do_login(self):
        try:
            self._init_header_data()
            self._user_check()
            self._verify_password()
            # 保存cookies 数据
            return self.save_cookie()
        except Exception:
            log.error('获取登录cookie,do_login报错', exc_info=True)
            return None


if __name__ == '__main__':
    log.info('do tb logining......')
    tb_username = ''
    tb_password = ''
    tb_ua = '123#LWFDbW+eHmDuJDbxlDlw8ldEzQXHO1A9926XjWVCQT/HzaHKDWDuwdtzsxIMrJOqvPY9SuqE9KEp2v8pp6A56WUU8nG6W5MfURlwEmeV1lmQvP4khn3n3U5LGdeH7kHzP8jYwFH0zd5BvyKg1j9aHbhLc0bot7VapBaoHrMcmu0F3Pz9OvjLH+eWTCtkTk9qf8Wes6wlHM4hCeRbPyDMl1y8L7sFsEOtDRH4gQyXxY3WetFwyslk4L6kIUKeTS5M/RRf671m/c8JaiT8A07AXxYKxmwdm5GAzyfgqgFhJFEy6nXV+ntJ+0RSh2Gh0KL/Z13iPBIhxf9/UoOZPhnUwH38UYd00I/zG3O7y+PNYzm1aOh3Xwo7SffoktkMiJN7KeXRsbCTUXeNHNMFvwLxu+9f7iOevqyTbfGd5T1daqTHtUj371MgvmU1X0i0H26XX6NKasWj8pCzGInkcCf4UJVboSWW1/zC2cpcChnchrMhMmh1HEe/qIX1BO4ZiXoUaBjGeCfY2KpXn9CFaqpJc0VbEO+9QHx8O0UQbbVJSQG8V9idJZDdz0mqzL7nA7aSMPmXQYaMy+wUxwStECjQGY1nUcv2o4b9y77yqJ57s35JqFuxI8jdbSvAsaKzS+4ZPD78LcNPlbvOLMrvRgMMYBrOwnVRnfuQGOI0OxR1tkU9kgsry1GhWl4JVzuhijkz9rZ+Qw5TOdAhq0HZGGB0eSpqLM5Kh+qoFQWGFCBhq1R9VH/EArOjBwXjSTcj0j6l5BRjAJBnBy3zAhOPZw20FYWD55vXBQ8N1fez5Hfgjr+/q44+RHiMUpWXOrTeKso6VdxQ1ydXMijNLPiw4D9Zg8SlBOgQ+eNJn13VRSeuEoLBT0rV+wVsXdMwzwXT1fW095buumtxpptrqPSfaz9HVpoNJQ0fCNQLhW8n/7lJ7zOGX0DPp5XaiW5HA6v0kySFiXFGiyG2xwzQmdx0TD3UynskxwaczF8+WYkkBONdQkuv5Ffrn4Sk3c4Kq45='
    tl = taobaoLogin(tb_username, tb_ua, tb_password)
    tl.do_login()
