import json
import requests
from cookiePool.redisdb import *


class zhuanliCookies(object):
    def __init__(self, username, password):
        self.url_index= 'https://www.patenthub.cn/'
        self.url_login= 'https://www.patenthub.cn/user/login.json'
        self.username = username
        self.password = password
        self.data = {
                    'redirect_to':self.url_index,
                    'sso':'',
                    'account':self.username,
                    'password':self.password,
                    }
        self.headers= {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'https://www.patenthub.cn/user/login.html',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection':'close',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Host': 'www.patenthub.cn',
        }
        self.session = requests.session()
        self.proxy = cookie_proxy()

    def get_home(self):
        global proxy
        while True:
            try:
                self.session.get(url=self.url_index, headers=self.headers, proxies=self.proxy, timeout=5)
                return self._login()
            except requests.exceptions.ConnectionError as r:
                r.status_code = "Connection refused"
                self.proxy = cookie_proxy()
            except Exception as e:
                print(e)
                self.proxy = cookie_proxy()

    def _login(self):
        while True:
            try:
                res = self.session.post(url=self.url_login, headers=self.headers, data=self.data, proxies=self.proxy, timeout=5).json()
                return res
            except requests.exceptions.ConnectionError as r:
                r.status_code = "Connection refused"
                self.proxy = cookie_proxy()
            except Exception as e:
                print(e)
                self.proxy = cookie_proxy()


    def get_cookies(self):
        return self.session.cookies.get_dict()

    def main(self):
        res = self._login()
        if res['success']:
            cookies = self.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
        else:
            if res['message'] == '用户名或密码错误':
                return {
                    'status': 0,
                    'content':'账号密码错误'
                }
            if res['message'] == '账号处于冻结状态，请重新注册并验证手机号码':

                return {
                    'status': 2,
                    'content':'账号处于冻结状态，请重新注册并验证手机号码'
                }


class CookiesGenerator(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies',self.website,'127.0.0.1',6379)
        self.accounts_db = RedisClient('accounts', self.website,'127.0.0.1',6379)

    def new_cookies(self, username, password):
        raise NotImplementedError

    def process_cookies(self, cookies):
        return cookies

    def run(self):
        accounts_usernames = self.accounts_db.usernames()
        print(accounts_usernames)
        cookies_usernames = self.cookies_db.usernames()

        for username in accounts_usernames:
            print(username)
            if not username in cookies_usernames:
                password = self.accounts_db.get(username)
                print('正在生成Cookies', '账号', username, '密码', password)
                result = self.new_cookies(username, password)
                if result.get('status') == 1:
                    cookies = self.process_cookies(result.get('content'))
                    print('成功获取到Cookies', cookies)
                    if self.cookies_db.set(username, json.dumps(cookies)):
                        print('成功保存Cookies')
                elif result.get('status') == 2:
                    print(result.get('content'))
                    if self.accounts_db.delete(username):
                        print('成功删除账号')
                elif result.get('status') == 0:
                    print(result.get('content'))
                    if self.accounts_db.delete(username):
                        print('成功删除账号')
                else:
                    print(result.get('content'))
        print('所有账号都已经成功获取Cookies')


class zhuanliCookiesGenerator(CookiesGenerator):
    def __init__(self, website='zhuanli'):
        CookiesGenerator.__init__(self, website)
        self.website = website
        print(self.website)

    def new_cookies(self, username, password):
        return zhuanliCookies(username, password).main()


if __name__ == '__main__':
    generator = zhuanliCookiesGenerator(website='zhuanli')
    generator.run()
