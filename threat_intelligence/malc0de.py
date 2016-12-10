# coding=utf-8

import csv
import bs4
import sys
import time
import pickle
import urllib.request

sys.setrecursionlimit(15000)


def marlware_data(result_list):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }
    page = 0

    while page < 14:
        url = 'http://malc0de.com/database/?&page=' + str(page)
        request = urllib.request.Request(url, headers=header)
        response = urllib.request.urlopen(request)
        content = response.read()
        result = bs4.BeautifulSoup(content, "html.parser")
        link = result.find_all('tr', {'class': "class1"})

        for item in link:
            result_list.append({'Date' : item.contents[1].contents[0].string,
                                'Domain' : item.contents[3].contents[0].string,
                                'IP' : item.contents[5].contents[0].string,
                                'CC': item.contents[7].contents[0].string,
                                'ASN': item.contents[9].contents[0].string,
                                'ASN_Name': item.contents[11].contents[0].string,
                                'MD5': item.contents[13].contents[0].string})

        page += 1
        time.sleep(2)

    with open('malcode.data', 'wb') as f:
        pickle.dump(result_list, f)

    return result_list


def extract():
    with open('malcode.data', 'rb') as f:
        data_list = pickle.load(f)

    print('抽取完毕！共抽出' + str(len(data_list)) +'个数据行.')

    with open('malcode_data.csv', 'w') as t:
        headers = ['Date', 'Domain', 'IP', 'CC', 'ASN', 'ASN_Name', 'MD5']
        writer = csv.DictWriter(t, headers)
        writer.writeheader()

        for item in data_list:
            writer.writerow(item)


if __name__ == "__main__":
    marlware_list = []
    marlware_list = marlware_data(marlware_list)
    extract()
