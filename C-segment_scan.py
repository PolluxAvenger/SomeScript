# coding=utf-8

import socket
import requests
from concurrent.futures import ThreadPoolExecutor


def worker(ip_address):
    global result_list

    #print('正在搜索' + ip_address)

    for port in range(1, 1025):
        link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        link.settimeout(2)
        status = link.connect_ex((str(ip_address), int(port)))

        if status == 0:
            result_list.append(str(ip_address + ':' + str(port)))


if __name__ == '__main__':
    result_list = []

    r = requests.get('http://ipinfo.io')
    result = r.json()
    ip_address = result['ip'].split('.')
    net_address = '.'.join(ip_address[:-1])

    # net_address = '123.58.180' 网易验证 180.149.134.141 新浪验证

    with ThreadPoolExecutor(max_workers=10) as executor:
        for item in range(1, 256):
            ip = '%s.%s' % (net_address, item)
            executor.submit(worker, ip)

    print(result_list)
