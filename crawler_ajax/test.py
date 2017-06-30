# coding=utf-8

import csv
import ssl
import json
import time
import random
import urllib.parse
import urllib.request


result_list = []

def write_csv(data, filename):
    with open(filename, 'w', encoding='utf-8-sig') as outf:
        dw = csv.DictWriter(outf, data[0].keys())
        dw.writeheader()
        for row in data:
            dw.writerow(row)


def get_data(id):
    global result_list
    ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://'

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
    }

    data = {}
    data['id'] = id

    request = urllib.request.Request(url, headers=header, data=urllib.parse.urlencode(data).encode('utf-8'))
    response = urllib.request.urlopen(request)
    content = response.read()
    result_data = json.loads(content.decode())
    result_list.append(result_data['Scan'])
    print('-----------------')
    time.sleep(random.randint(3,10))


if __name__ == '__main__':
    for id_number in range(100, 500):
        print('Start: ' + str(id_number))
        try:
            get_data(id_number)
        except Exception as e:
            continue

    print(str(len(result_list)))
    write_csv(result_list, 'result.csv')
