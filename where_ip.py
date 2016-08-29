# coding=utf-8

import requests


'''
    查询公网 IP 地址的相关接口
    ip.cn
    ipinfo.io
    cip.cc
    ifconfig.me
    myip.ipip.net
'''


def where_ip():
    r = requests.get('http://ipinfo.io')
    result = r.json()
    print('IP 地址为：' + result['ip'] + '位于：' + result['country'] + '的' + result['city'] + '市(' + result['loc'] + ')')


if __name__ == '__main__':
    where_ip()
