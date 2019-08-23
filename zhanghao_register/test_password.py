"""
    @author: 王帅帅
    @project: zhuanlihui
    @file: test_password.py
    @time: 2019/8/19/019 9:02
    @desc:
"""
import re, random, string

# count1 = int(input('请输入密码个数(必须大于0)： '))
# i = 0


def get_password():
    while True:
        tmp = random.sample(string.ascii_letters + string.digits, random.randint(6,18))
        passwd = ''.join(tmp)
        if re.search('[0-9]', passwd) and re.search('[A-Z]', passwd) and re.search('[a-z]', passwd):
            return passwd
        else:
            pass

if __name__ == '__main__':
    print(get_password())