# coding=utf-8

import os
import bs4
import sys
import pickle
import urllib
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.setrecursionlimit(12000)


def save_ip(ip_object, dir_name, word):
    ip_list = []
    file_name = word + '_ip.dat'
    file_locate = os.path.join(dir_name, word, file_name)

    for item in ip_object:
        ip_list.append(str(item.string))

    with open(file_locate, 'wb') as t:
        pickle.dump(ip_list, t)


def save_md5(md5_object, dir_name, word):
    md5_list = []
    file_name = word + '_md5.dat'
    file_locate = os.path.join(dir_name, word, file_name)

    for item in md5_object:
        md5_list.append(str(item.string))

    with open(file_locate, 'wb') as t:
        pickle.dump(md5_list, t)


def save_domain(domain_object, dir_name, word):
    domain_list = []
    file_name = word + '_domain.dat'
    file_locate = os.path.join(dir_name, word, file_name)

    for item in domain_object:
        domain_list.append(str(item.string))

    with open(file_locate, 'wb') as t:
        pickle.dump(domain_list, t)


def extract_ip(file_path='/root/PycharmProjects/untitled/gcman/gcman_domain.dat'):
    ip_list = []
    print(file_path)

    with open(file_path, 'rb') as f:
        ip_list = pickle.load(f)

    for item in ip_list:
        print(item)


def url_ioc(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36',
    }

    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    content = response.read()
    result = bs4.BeautifulSoup(content, "xml")

    result_name = result.find('short_description')
    ioc_name = result_name.string

    base_dir = os.getcwd()
    base_name = os.path.join(base_dir, ioc_name)

    if not os.path.exists(base_name):
        os.mkdir(ioc_name)

    ioc_ip = result.find_all('Content', type="IP")
    save_ip(ioc_ip, base_dir, ioc_name)
    ioc_md5 = result.find_all('Content', type="md5")
    save_md5(ioc_md5, base_dir, ioc_name)
    ioc_domain = result.find_all('Content', type="string")
    save_domain(ioc_domain, base_dir, ioc_name)


if __name__ == '__main__':
    ioc_list = ['https://securelist.com/files/2016/02/Metel.ioc', 'https://securelist.com/files/2016/02/Gcman-AttackAgainstFinancialInstitutions.ioc']

    with ThreadPoolExecutor(max_workers=2) as executor:
        for item in ioc_list:
            executor.submit(url_ioc, item)

    extract_ip()
    print('Game Over!')
