# coding=utf-8

import csv
import bs4
import time
import pickle
import urllib.request


def marlware_data(result_list):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }
    start_line = 0

    while start_line < 32000:
        url = 'http://vxvault.net/ViriList.php?s=' + str(start_line) + '&m=400'
        request = urllib.request.Request(url, headers=header)
        response = urllib.request.urlopen(request)
        content = response.read()
        result = bs4.BeautifulSoup(content, "html.parser")
        link = result.find_all('tr')
        count = 0

        for item in link:
            if not count:
                count += 1
                continue

            count += 1

            result_list.append({'Date' : item.contents[1].contents[0].text,
                                'MD5' : item.contents[5].contents[0].text,
                                'IP' : item.contents[7].contents[0].text})

        start_line += 400
        time.sleep(3)

    with open('malware.data', 'wb') as f:
        pickle.dump(result_list, f)

    return result_list


def extract():
    with open('malware.data', 'rb') as f:
        data_list = pickle.load(f)

    print('抽取完毕！共抽出' + str(len(data_list)) +'个数据行.')

    with open('malware_data.csv', 'w') as t:
        headers = ['Date', 'MD5', 'IP']
        writer = csv.DictWriter(t, headers)
        writer.writeheader()

        for item in data_list:
            writer.writerow(item)


if __name__ == "__main__":
    marlware_list = []
    marlware_list = marlware_data(marlware_list)
    extract()
