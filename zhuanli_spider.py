"""
    @author: 王帅帅
    @project: zhuanlihui
    @file: demo01_spider.py
    @time: 2019/8/8/008 9:46
    @desc:
"""
import requests.adapters
import re
import json

from function import *
from cookiePool.redisdb import *
from bs4 import BeautifulSoup as BS
import hashlib
from pymongo.errors import DuplicateKeyError
import time
import pika

conn = RedisClient('cookies', 'zhuanli')
def get_cookie():
    cookies = json.loads(conn.random())
    cookie = 'U_TOKEN=%s;s=%s;'%(cookies['U_TOKEN'],cookies['s'])
    return cookie

def get_data(url):
    proxy = get_proxy()
    while True:
        headers = {
            'Connection':'close',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Host': 'www.patenthub.cn',
            'Cookie': 'U_TOKEN=9b061130b7158892a9b72a6c72c336c12e814499;s=W0U6Ux9Wdnh+fVQOB1IhLxNXJy8MAFcoFUQVTwEpQxhLFTxeLkZEJjBVVQ4ZH09JHxoPTlxHWnMXFz0=;'
        }
        try:
            base_resp = requests.get(url=url, headers=headers,proxies=proxy, timeout=5)
            title = re.findall(r'<title>(.*?)</title>',base_resp.text)[0]
            if '用户登录' in title or '重复登录'in title:
                return {
                    'status': 0,
                    'content': '账号失效'
                }
            elif "PatentHub_404页面" in title:
                return {
                    'status': 2,
                    'content': '无次信息'
                }
            else:
                print(title)
                claims_resp = requests.get(url=url + '/claims', headers=headers, proxies=proxy, timeout=5).text
                description_resp = requests.get(url=url + '/description', headers=headers, proxies=proxy,
                                                timeout=5).text
                transaction_resp = requests.get(url=url + '/transaction', headers=headers, proxies=proxy,
                                                timeout=5).text
                base_text = BS(base_resp.text, 'lxml')
                claims_text = BS(claims_resp, 'lxml')
                description_text = BS(description_resp, 'lxml')
                transaction_text = BS(transaction_resp, 'lxml')
                name = re.findall(r'<title>专利汇 - (.*?) - PatentHub专利检索|专利汇|专利查询网|发明专利查询分析</title>', base_resp.text)[0]
                id = hashlib.md5(name.encode()).hexdigest()
                base = str(base_text.find(id='detail-page'))
                claims = str(claims_text.find(class_='content description'))
                description = str(description_text.find(class_='content description'))
                transaction = str(transaction_text.find(class_='ui celled striped table'))
                number = re.findall('https://www.patenthub.cn/patent/(.*)', url)[0]
                data = {
                    '_id': id,
                    'number':number,
                    'name': name,
                    'base': base,
                    'claims': claims,
                    'description': description,
                    'transaction': transaction
                }
                try:
                    db.test0813.insert_one(data)
                except DuplicateKeyError as D:
                    pass
                requests.adapters.DEFAULT_RETRIES = 5
                return {
                    'status': 1,
                    'content': '获取信息成功'
                }
        except requests.exceptions.ConnectionError as r:
            r.status_code = "Connection refused"
            proxy = get_proxy()
        except Exception as e:
            print(e)
            proxy = get_proxy()
        time.sleep(1)


def start():
    queue = 'wss_zhuanlihui'
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        '192.168.1.157', 5672, '/', credentials, heartbeat=2000))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    def callback(ch, method, properties, body):
        if body.decode('utf-8') =='CN109162054A':
            time.sleep(3600)
        data_id = body.decode('utf-8')
        print('查询信息：', data_id)
        try:
            url = 'https://www.patenthub.cn/patent/'+ data_id
            check = get_data(url)
            print(check)
            if check['status'] == 0:
                ch.basic_nack(delivery_tag=method.delivery_tag)
                return
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

        except AttributeError:
            # redis 中 cookie 完了
            print("redis队列为空：AttributeError")
            channel.close()

    # 公平调度
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue, callback)
    channel.start_consuming()


if __name__ == '__main__':
    start()

