import redis
from pymongo import MongoClient


def conRedis():
    return redis.Redis(host='192.168.1.157', port=6379)

redis_client = conRedis()


def conMongo():
    conMongo = MongoClient(host='192.168.1.170', port=27017)
    return conMongo


db = conMongo().wss_zhuanlihui
GS_db = conMongo().GsApp

def w_csv(path, data):
    with open(path, 'a', encoding="utf-8") as f:
        f.write(data)

def r_csv(path):
    with open(path, 'r', encoding="utf-8") as f:
        data = f.read()
    return data

'''{'url':{'$regex':'^https'}}'''

def tiqu_data():
    data = db.test360.find({'url':{'$lte':5}})
    return data


def get_ip():
    ip = redis_client.brpop('test_proxy', 0)[1]
    ip = ip.decode('utf-8')
    proxy = {"http": "http://pig444:1234as@"+ip,"https": "https://pig444:1234as@"+ip}
    # proxy = {"http": 'http://' + ip, "https": 'https://' + ip}
    print('ip地址：', ip)
    return ip

def get_proxy():
    ip = redis_client.brpop('test_proxy', 0)[1]
    ip = ip.decode('utf-8')
    proxy = {"http": "http://pig444:1234as@"+ip,"https": "https://pig444:1234as@"+ip}
    # proxy = {"http": 'http://' + ip, "https": 'https://' + ip}
    print('ip地址：', ip)
    return proxy







# if __name__ == '__main__':
    # get_cookie()


















