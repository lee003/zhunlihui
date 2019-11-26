import redis
import random
from cookiePool.config import *

class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        return "{type}:{website}".format(type=self.type,website=self.website)

    def set(self, username, value):
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        return self.db.hget(self.name(), username)

    def delete(self, username):
        return self.db.hdel(self.name(), username)

    def count(self):
        return self.db.hlen(self.name())

    def random(self):
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        return self.db.hkeys(self.name())

    def all(self):
        return self.db.hgetall(self.name())


def set(username):
    password ='1234AS'
    result = conn.set(username, password)
    print('账号', username, '密码', password)
    print('录入成功' if result else '录入失败')


def scan():
    print('请输入账号密码组，输入exit退出读入:')
    while True:
        account = input()
        if account == 'exit':
            break
        set(account)


if __name__ == '__main__':
    conn = RedisClient('accounts', 'zhuanli')
    # print(conn.usernames())
    scan()
