# coding=utf-8

import csv
import bs4
import sys
import time
import pickle
import random
import urllib
import urllib.request

sys.setrecursionlimit(45000)


def extract_information(result_list, max_page = 10):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }
    page = 0

    while page < max_page:
        name_list = []
        date_list = []
        org = page * 30
        url = 'http://securityfocus.com/cgi-bin/index.cgi?o=' + str(org) + '&l=30&c=12&op=display_list&vendor=&version=&title=&CVE='
        request = urllib.request.Request(url, headers=header)
        try:
            response = urllib.request.urlopen(request, timeout=250)
        except Exception as e:
            continue
        content = response.read()
        result = bs4.BeautifulSoup(content, "html.parser")
        a_link = result.find_all('a')
        span_link = result.find_all('span', {'class': "date"})

        count = 0
        for item in a_link:
            if count < 13 or count > 73:
                count += 1
                continue
            if item.text == 'Next >':
                count += 1
                continue
            name_list.append(item.text)
            count += 1

        for item in span_link:
            date_list.append(item.text)

        name_count = 0
        name_copy = ''
        name_judge = True
        for item in name_list:
            if name_judge == True:
                name_copy = item
                name_judge = False
            else:
                result_list.append({'Name': name_copy,
                                    'Date': date_list[name_count],
                                    'Link': item})
                name_count += 1
                name_judge = True

        page += 1
        print('进入等待，准备进入下一页!')
        time.sleep(random.randint(5, 20))

    with open('information_list.data', 'wb') as f:
        pickle.dump(result_list, f)

    return result_list


def extract_data():
    with open('information_list.data', 'rb') as f:
        data_list = pickle.load(f)

    print('抽取完毕！共抽出' + str(len(data_list)) +'个数据行.')

    with open('information_list.csv', 'w', newline='') as t:
        headers = ['Name', 'Date', 'Link']
        writer = csv.DictWriter(t, headers)
        writer.writeheader()

        for item in data_list:
            writer.writerow(item)


if __name__ == "__main__":
    information_list = []
    information_data = extract_information(information_list, 1000)
    print('一共有' + str(len(information_data)) + '条数据')
    extract_data()
