from flask import Flask, g
import json
from cookiePool.redisdb import *


__all__ = ['app']

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'

def get_conn():
    for website in GENERATOR_MAP:
        print(website)
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies","' + website + '")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts", "' + website + '")'))
    return g

@app.route('/<website>/cookie')
def random(website):
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies

@app.route('/<website>/add/<username>/<password>')
def add(website, username, password):
    g = get_conn()
    print(username, password)
    getattr(g, website + '_accounts').set(username, password)
    return json.dumps({'status': '1'})

@app.route('/<website>/count')
def count(website):
    g = get_conn()
    count = getattr(g, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})


if __name__ == '__main__':
    app.run(host='127.0.0.1')





















