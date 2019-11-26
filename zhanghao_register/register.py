import requests
from function import *
import time
from zhanghao_register.chaojiying import Chaojiying_Client
from urllib.parse import urlparse,parse_qs
from cookiePool.redisdb import *
import datetime
import re, random, string

conn = RedisClient('accounts', 'zhuanli')


proxy = get_proxy()
session = requests.session()
url_index = 'https://www.patenthub.cn'
url_resiger = 'https://www.patenthub.cn/user/register/one.html'
url_code = 'https://www.patenthub.cn/authImage?t=%s'%(int(time.time()))
url_end = 'https://www.patenthub.cn/user/register/two.html'
TOKEN = '00489558122a6869dfd207135512812c2d74107ecf01'
PROJECT =  '20740'

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.patenthub.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://www.patenthub.cn/',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
}

data = {
        'redirect_to':'',
        'sso':'',
        'account': '',
        'realName': '',
        'password': '',
        'rePass': '',
        'enterpriseName': '',
        'worker': '',
        'code': '',
        'accept': '1'
}

phone_data = {
            'redirect_to':'',
            'sso':'',
            'account': '',
            'code': '',
            'token': ''
}

zhiwei = ['总裁','董事长','首席执行官','副总经理','人力资源总监','财务总监','首席财务官','营销总监','市场总监','销售总监','生产总监','运营总监','首席运营官','技术总监','首席技术官','总经理助理','技术主管','技术支持经理','研发主管','产品规划主管','产品开发工程师','产品开发技术员','产品质量工程师','质量工程师','工艺工程师','电气工程师','电子工程师','食品工程师','环境检测工程师','环境治理工程师','通讯测试工程师','通讯工程师','硬件工程师','部件工程师','安全工程师', '安全员', '包装设计师', '材料工程师', '模具工程师', '机械工程师', '布线工程师', '系统开发工程师', '计算机管理员', '软件工程师', '测试主管', '系统测试工程师', '软件测试工程师', '数据库工程师', '高级程序员', '系统应用工程师', '系统分析员', '系统操作员', '网络工程师', '网络管理工程师', '网络管理员', '网络安全工程师', '工程技术项目经理', '质量监督工程师', '质量监督员','安全监督员','检测员', '造价工程师', '建筑设计师', '土木建筑工程师','结构设计工程师','道路桥梁工程师', '园林工程师', '城镇规划设计工程师','水利水电工程师','给排水工程师','暧通工程师','网站主编']


def get_phone():
    while True:
        try:
            url = 'http://i.fxhyd.cn:8080/UserInterface.aspx?action=getmobile&token=%s&itemid=%s'%(TOKEN, PROJECT)
            phone = requests.get(url)
            if 'success' in phone.text:
                return re.findall('success\|(.*)', phone.text)[0]
            else:
                print(phone.text)
        except Exception as e:
            print('获取手机号码错误',e)
        time.sleep(0.1)

def get_phone_code(number):
    while True:
        try:
            url = 'http://i.fxhyd.cn:8080/UserInterface.aspx?action=getsms&token=%s&itemid=%s&mobile=%s&release=1' % (
            TOKEN, PROJECT, number)
            phone = requests.get(url)
            if 'success' in phone.text:
                text = re.findall('success\|(.*)', phone.text)[0]
                return re.findall(r'【专利汇】您的验证码是：(.*?)，5分钟内有效！',text)[0]
            elif phone.text == '2007':
                print('号码被释放',phone.text)
                break
            else:
                print(phone.text)
        except Exception as e:
            print('获取手机验证码错误',e)
        time.sleep(2)


def get_base_info():
    with open('./company_info.txt','r',encoding='utf-8') as f:
        data = eval(f.read())
    info = random.choice(data)
    name = info['baseinfo']['data']['legalPersonName']
    gs_name = info['baseinfo']['data']['name']
    return (name, gs_name)


def get_password():
    while True:
        tmp = random.sample(string.ascii_letters + string.digits, random.randint(6,18))
        passwd = ''.join(tmp)
        if re.search('[0-9]', passwd) and re.search('[A-Z]', passwd) and re.search('[a-z]', passwd):
            return passwd
        else:
            pass



def parse_code(code):
    chaojiying = Chaojiying_Client('pig444', '1234as', '896632')
    code = chaojiying.PostPic(code.content, 1902)
    return code['pic_str']


def get_home(account,realName,password,rePass,enterpriseName,worker):
    global proxy
    while True:
        try:
            session.get(url=url_index, headers=headers, proxies=proxy, timeout=3)
            return _resiger(account,realName,password,rePass,enterpriseName,worker)
        except requests.exceptions.ConnectionError as r:
            r.status_code = "Connection refused"
            proxy = get_proxy()
        except Exception as e:
            print(e)


def _resiger(account,realName,password,rePass,enterpriseName,worker):
    while True:
        try:
            session.get(url=url_resiger, headers=headers, proxies=proxy, timeout=5)
            get_code = session.get(url = url_code, headers= headers,proxies= proxy, timeout=5)
            data['code'] = parse_code(get_code)
            data['account'] = account
            data['realName'] = realName
            data['password'] = password
            data['rePass'] = rePass
            data['enterpriseName'] = enterpriseName
            data['worker'] = worker
            print(data)
            put_info = session.post(url=url_resiger, headers=headers, proxies=proxy, data= data,timeout=5)
            if put_info.json()['success']:
                uri = url_index + put_info.json()['uri']
                print(uri)
                phone_code = get_phone_code(account)
                number = phone_code
                phone_data['account'] = account
                phone_data['code']= number
                phone_data['token'] = parse_qs(urlparse(uri).query)['token'][0]
                print(phone_data)
                phone_yanzheng = session.post(url=url_end, headers=headers, proxies=proxy, data= phone_data,timeout=3)
                print(phone_yanzheng.json())
                if phone_yanzheng.json()['success']:
                     conn.set(account, password)
                     with open('./register.txt', 'a',encoding='utf-8') as f:
                         f.write(account +':'+ password + ';')
                break
            elif put_info.json()['message'] == '账号已经存在':
                account = get_phone()
            else:
                print('页面请求不成功',put_info.json())
        except requests.exceptions.ConnectionError as r:
            r.status_code = "Connection refused"
            # proxy = get_proxy()
        except Exception as e:
            print(e)

def main():
    count = 0
    while count< 4:
        now = datetime.datetime.now()
        password = get_password()
        account = get_phone()
        realName, enterpriseName = get_base_info()
        worker = random.choice(zhiwei)
        if account:
            get_home(account, realName, password, password, enterpriseName, worker)
        else:
            print('获取号码失败')
        time_sleep = random.randint(200,500)
        print(now, time_sleep)
        time.sleep(time_sleep)
        count += 1


if __name__ == '__main__':
    main()





