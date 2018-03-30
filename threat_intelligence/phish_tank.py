# coding=utf-8

import re
import csv
import bs4
import sys
import ssl
import time
import pickle
import random
import requests
import urllib.request
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


sys.setrecursionlimit(15000)


class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def phish_data(result_list, page_max = 50):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }
    page = 0

    while page < page_max:
	    s = requests.Session()
        s.mount('https://', MyAdapter())
        url = 'https://www.phishtank.com/phish_search.php?page=' + str(page) + '&active=y&verified=u'
        response = s.get(url)
        content = response.text
        result = bs4.BeautifulSoup(content, "html.parser")
        link = result.find_all('tr')

        count = 0
        for item in link:
            if not count:
                count += 1
                continue

            count += 1
            regular = re.compile('added on (.+)')
            date = regular.split(item.contents[1].contents[2].string)[1]
            result_list.append({'Date': date,
                                'URL': item.contents[1].contents[0].string})

        page += 1
        time.sleep(random.randint(1, 10))

    with open('phish_tank.data', 'wb') as f:
        pickle.dump(result_list, f)

    return result_list


def extract():
    with open('phish_tank.data', 'rb') as f:
        data_list = pickle.load(f)

    print('抽取完毕！共抽出' + str(len(data_list)) + '个数据行.')

    with open('phish_tank.csv', 'w', newline='', encoding='utf-8') as t:
        headers = ['Date', 'URL']
        writer = csv.DictWriter(t, headers)
        writer.writeheader()

        for item in data_list:
            writer.writerow(item)


if __name__ == "__main__":
    marlware_list = []
    marlware_list = phish_data(marlware_list, 10)
    extract()