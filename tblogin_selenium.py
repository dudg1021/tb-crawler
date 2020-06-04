#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: diange.du
@file: tblogin_selenium.py
@time: 2020/6/3 16:50
@desc: chromedriver方式登录
'''
import time
from utils.config import *
from utils.logutil import log
from selenium import webdriver
from selenium.webdriver import ActionChains  # 动作链


class TaoBaoLoginSelenium:
    def __init__(self):
        pass

    def do_login(self, u_name, u_pwd):
        # 为了防止你不确定自己的 chrom 版本，最好两个混合用
        options = webdriver.ChromeOptions()
        # chrom在79版之前用这个
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # =>linux环境 为Chrome配置无头模式
        # options.add_argument("--headless")
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--disable-dev-shm-usage')
        # 这个是更改 user-agent 的，可有可无
        options.add_argument(
            "user-agent=Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")
        chrome = webdriver.Chrome(options=options)
        # chrom在79版之后用这个
        chrome.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                  """
        })
        log.info('step-1 打开登录页...')
        chrome.get('https://login.taobao.com/member/login.jhtml?')  # 发送请求,打开淘宝登录地址
        log.info('sleep 2秒等待网页加载...')
        time.sleep(2)  # 等待加载,网络不好的话页面信息加载不出来,可以根据网速自行设定

        username_input = chrome.find_element_by_id("fm-login-id")  # 获取用户名输入窗口
        password_input = chrome.find_element_by_id("fm-login-password")  # 获取密码输入窗口

        log.info('step-2 输入用户名密码...')
        username_input.send_keys(u_name)  # 输入用户名
        password_input.send_keys(u_pwd)  # 输入密码
        log.info('sleep 2秒等待加载滑块...')
        time.sleep(2)  # 等待加载,这里会加载滑块

        log.info('step-3 获取并拖动滑块...')
        slider = chrome.find_element_by_xpath("//*[@id='nc_1_n1z']")
        action = ActionChains(chrome)  # 创建动作链
        action.click_and_hold(slider)  # 模拟按住滑块不松开
        try:
            action.move_by_offset(258, 0).perform()  # 拖动滑块到底,通过浏览器可以获取拖动的距离
        except:
            log.error("拖动滑块异常", exc_info=True)
            pass
        action.release()  # 释放动作链
        log.info('拖动滑块后等待js校验...')
        time.sleep(2)
        # login_button = chrome.find_element_by_xpath(
        #     "/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[4]/button")  # 获取登录按钮
        # login_button.click()  # 点击登录
        chrome.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
        log.info('step-4 点击登录,sleep 10s 环境检测...')
        # 等待登录检测和重定向
        time.sleep(10)
        html = chrome.page_source  # 获取登录后页面信息
        # 重定向到导购后台取接口相关token
        html = chrome.get(
            'https://market.m.taobao.com/app/ulife/pc-guider-static/tb-live-data/index.html?spm=a1z9u.8142865.0.0.7e7434edeYvbrZ')
        # 等待页面加载
        time.sleep(5)
        log.info('step-5 获取cookie...')
        cookie_str = self.get_cookies(chrome)
        # 关闭chromedriver
        chrome.close()
        return cookie_str

    def get_cookies(self, chrome):
        chrome_cookies = chrome.get_cookies()  # 获取cookies
        print(chrome_cookies)
        cookie_str = ''
        cookie_dict = {}
        for cookie in chrome_cookies:
            cookie_str += '{}={};'.format(cookie['name'], cookie['value'])
            cookie_dict[cookie['name']] = cookie['value']
        log.info('cookie_str>>> '+cookie_str)
        # print(cookie_dict)
        return cookie_str


def get_login_cookies():
    log.info('do tb logining......')
    tl = TaoBaoLoginSelenium()
    return tl.do_login('', '')


if __name__ == '__main__':
    TaoBaoLoginSelenium().do_login('', '')
