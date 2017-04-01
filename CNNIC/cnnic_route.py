# coding=utf-8

import bs4
import pickle
import urllib.request


def route_data(route_info, result_list):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }

    url = 'http://ipwhois.cnnic.net.cn/bns/query/Query/ipwhoisQuery.do?txtquery=' + route_info + '&queryOption=route'
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    content = response.read()
    result = bs4.BeautifulSoup(content, "html.parser")
    link = result.find_all('tr')
    count = 0

    for item in link:
        count += 1
        if item.contents[1].text.split(':')[0] == '':
            continue
        elif count <= 13:
            result_list.append({item.contents[1].text.split(':')[0]: item.contents[3].text.replace(u'\xa0', '')})
        elif count >= 15 and count <= 21:
            result_list.append({item.contents[1].text.split(':')[0]: item.contents[3].text.replace(u'\xa0', '')})
        elif count >= 23 and count <= 32:
            result_list.append({item.contents[1].text.split(':')[0] + '-1': item.contents[3].text.replace(u'\xa0', '')})
        elif count >= 34 and count <= 43:
            result_list.append({item.contents[1].text.split(':')[0] + '-2': item.contents[3].text.replace(u'\xa0', '')})
        elif count > 43:
            break
        else:
            result_list.append({item.contents[1].text.split(':')[0]: item.contents[3].text.replace(u'\xa0', '')})

    with open('cnnic_route.data', 'wb') as f:
        pickle.dump(result_list, f)

    return result_list


if __name__ == "__main__":
    data_list = []
    data_list = route_data('211.144.211.0/24', data_list)
    print(data_list)
