# coding=utf-8

import bs4
import pickle
import urllib.request


def ipv4_data(ipv4, result_list):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }

    url = 'http://geoip.neu.edu.cn/?ip=+' + ipv4
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    content = response.read()
    result = bs4.BeautifulSoup(content, "html.parser")
    link = result.find_all('div', {'class': "row"})
    count = 0

    for item in link:
        if count == 4:
            address_list = item.text.split('\n\n')
            result_list.append({'教育网地址': address_list[2].strip()})
        if count == 5:
            address_list = item.text.split('\n\n')
            result_list.append({'免费地址': address_list[2].strip()})
        if count == 6:
            address_list = item.text.split('\n\n')
            result_list.append({'纯真地址': address_list[2].strip()})
        if count == 7:
            address_list = item.text.split('\n\n')
            result_list.append({'GeoIP': address_list[2].strip()})

        count += 1

    with open('neu_ipv4.data', 'wb') as f:
        pickle.dump(result_list, f)

    return result_list


if __name__ == "__main__":
    data_list = []
    data_list = ipv4_data('219.224.52.238', data_list)
