# coding=utf-8

import csv
import sys
import json
import pickle
import requests

sys.setrecursionlimit(15000)


def reverse_ip(ip_address):
    result_list = []

    payload = {'remoteAddress': ip_address, 'key': '', '_': ''}
    r = requests.post('http://domains.yougetsignal.com/domains.php', data=payload)
    content = json.loads(r.text)

    if content['status'] == 'Success':
        domain_list = content['domainArray']

        for item in domain_list:
            result_list.append({'IP': ip_address, 'Domain': item[0]})

        with open('same_ip_domain.data', 'wb') as f:
            pickle.dump(result_list, f)

        return (ip_address, result_list)

    else:
        print('查询失败！')


def extract():
    with open('same_ip_domain.data', 'rb') as f:
        data_list = pickle.load(f)

    print('抽取完毕！共有' + str(len(data_list)) +'个旁站域名.')

    with open('same_ip_domain.csv', 'w', newline='', encoding='utf-8') as t:
        headers = ['IP', 'Domain']
        writer = csv.DictWriter(t, headers)
        writer.writeheader()

        for item in data_list:
            writer.writerow(item)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        ip_address, marlware_list = reverse_ip(sys.argv[1])
        extract()
    else:
        print("usage: %s host" % sys.argv[0])
        sys.exit(-1)
