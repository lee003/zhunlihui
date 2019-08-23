"""
    @author: 王帅帅
    @project: zhuanlihui
    @file: config.py
    @time: 2019/8/12/012 14:16
    @desc:
"""

# Redis 数据库地址
REDIS_HOST = '127.0.0.1'
# Redis 端口
REDIS_PORT = 6379
# Redis密码，无密码就为 None
REDIS_PASSWORD = None

# 产生器使用的浏览器
BROWSER_TYPE = 'Chrome'

# 产生器类，如要扩展其他站点，就在这里配置
GENERATOR_MAP = {
    'zhuanli': 'zhuanliCookiesGenerator',
}

# 测试类，如要扩展其他站点，就在这里配置
TESTER_MAP = {
    'zhuanli': 'ZhuanliValidTester',
}

TEST_URL_MAP = {
    'zhuanli': 'https://www.patenthub.cn/patent/CN109111000A',
}

# 产生器和验证器循环周期
CYCLE = 120

# API地址和端口
API_HOST = '127.0.0.1'
API_PORT = 5000

# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = False
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
# API接口服务
API_PROCESS = False


# ip
import redis
def cookie_conRedis():
    return redis.Redis(host='192.168.1.157', port=6379)

redis_client = cookie_conRedis()
def cookie_ip():
    ip = redis_client.brpop('test_proxy', 0)[1]
    ip = ip.decode('utf-8')
    proxy = {"http": "http://pig444:1234as@"+ip,"https": "https://pig444:1234as@"+ip}
    # proxy = {"http": 'http://' + ip, "https": 'https://' + ip}
    print('ip地址：', ip)
    return ip
def cookie_proxy():
    ip = redis_client.brpop('test_proxy', 0)[1]
    ip = ip.decode('utf-8')
    proxy = {"http": "http://pig444:1234as@"+ip,"https": "https://pig444:1234as@"+ip}
    # proxy = {"http": 'http://' + ip, "https": 'https://' + ip}
    print('ip地址：', ip)
    return proxy
