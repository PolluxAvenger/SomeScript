# coding=utf-8

import bs4
import pickle
import urllib.request


def mac_data(ipv4, result_list):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }

    url = 'http://apps.neu.edu.cn/macquery/?mac=' + ipv4
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    content = response.read()
    result = bs4.BeautifulSoup(content, "html.parser")
    link = result.find_all('span', {'class': "span5"})
    count = 0

    for item in link:
        if count == 0:
            result_list.append({'MAC地址': item.text})
        if count == 1:
            result_list.append({'所属地址块': item.text})
        if count == 2:
            result_list.append({'所属公司': item.text})
        if count == 3:
            result_list.append({'公司地址': item.text})
        if count == 4:
            result_list.append({'国家代码': item.text})

        count += 1

    with open('neu_mac.data', 'wb') as f:
        pickle.dump(result_list, f)

    return result_list


if __name__ == "__main__":
    data_list = []
    data_list = mac_data('08-00-27-0E-25-B8', data_list)
