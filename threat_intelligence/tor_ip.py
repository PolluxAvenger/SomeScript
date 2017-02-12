# coding=utf-8

import os
import requests


def dan_list(url):
    r = requests.get(url, stream=True)
    file_name = os.path.join(os.getcwd(), 'tor', 'tor_exist_ip.txt')
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    with open(file_name, "wb") as t:
        t.write(r.content)


if __name__ == '__main__':
    # 此链接每三十分钟才能请求一次，为当前 Tor 节点的列表
    dan_list('https://www.dan.me.uk/torlist/?exit')
