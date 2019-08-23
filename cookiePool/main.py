"""
    @author: 王帅帅
    @project: zhuanlihui
    @file: wss_main.py
    @time: 2019/8/12/012 15:14
    @desc:
"""
from cookiePool.scheduler import Scheduler
def main():
    s = Scheduler()
    s.run()

if __name__ == '__main__':
    main()