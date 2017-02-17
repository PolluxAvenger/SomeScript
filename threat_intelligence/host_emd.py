# coding=utf-8

import csv
import bs4
import sys
import time
import pickle
import random
import urllib.request

sys.setrecursionlimit(45000)


def marlware_data(result_list):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }
    page = 1

    while page < 3:
        url = 'https://hosts-file.net/?s=Browse&f=EMD&d=&o=DESC&page=' + str(page)
        request = urllib.request.Request(url, headers=header)
        response = urllib.request.urlopen(request)
        content = response.read()
        result = bs4.BeautifulSoup(content, "html.parser")
        link = result.find_all('tr')
        count = 0
        for item in link:
            if count < 8 or count > 107:
                count += 1
                continue

            line_result = item.text.split(' ')
            result_list.append({'Domain' : line_result[2],
                                'IP' : line_result[3],
                                'Type' : line_result[4],
                                'Date': line_result[5]})

        page += 1
        print('进入等待!')
        time.sleep(random.randint(5, 20))

    with open('host_emd.data', 'wb') as f:
        pickle.dump(result_list, f)

    return result_list


def extract():
    with open('host_emd.data', 'rb') as f:
        data_list = pickle.load(f)

    print('抽取完毕！共抽出' + str(len(data_list)) +'个数据行.')

    with open('host_emd.csv', 'w', newline='') as t:
        headers = ['Domain', 'IP', 'Type', 'Date']
        writer = csv.DictWriter(t, headers)
        writer.writeheader()

        for item in data_list:
            writer.writerow(item)


if __name__ == "__main__":
    marlware_list = []
    marlware_list = marlware_data(marlware_list)
    print('一共有' + str(len(marlware_list)) + '条数据')
    extract()
