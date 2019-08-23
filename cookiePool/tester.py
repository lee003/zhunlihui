"""
    @author: 王帅帅
    @project: zhuanlihui
    @file: tester.py
    @time: 2019/8/12/012 14:28
    @desc:
"""
import json
from cookiePool.redisdb import *
from cookiePool.config import *

import re
import requests



class ValidTester(object):
    def __init__(self, website='defult'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website, '127.0.0.1', 6379)
        self.accounts_db = RedisClient('accounts', self.website, '127.0.0.1', 6379)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class ZhuanliValidTester(ValidTester):
    def __init__(self, website='zhuanli'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username)
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return
        proxy = cookie_proxy()
        while True:
            try:
                test_url = 'https://www.patenthub.cn/patent/CN109111005A'
                cookie= 'U_TOKEN=%s;s=%s;'%(cookies['U_TOKEN'],cookies['s'])
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                    'Host': 'www.patenthub.cn',
                    'Cookie': cookie
                }
                response = requests.get(url=test_url, headers=headers, cookies=cookies, timeout=2, proxies=proxy)
                title = re.findall(r'<title>(.*?)</title>', response.text)[0]
                if title:
                    print(title)
                    if '用户登录' in title or '重复登录'in title:
                        print(response.status_code, response.headers)
                        print('Cookies失效', username)
                        self.cookies_db.delete(username)
                        print('删除Cookies', username)
                    else:
                        print('Cookies有效', username)
                    break
            except requests.exceptions.ConnectionError as r:
                r.status_code = "Connection refused"
                proxy = cookie_proxy()
            except Exception as e:
                print('发生异常', e.args)
                proxy = cookie_proxy()


if __name__ == '__main__':
    ZhuanliValidTester('zhuanli').run()


