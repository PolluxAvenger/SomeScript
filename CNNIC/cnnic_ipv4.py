# coding=utf-8

import bs4
import pickle
import urllib.request


def ipv4_data(ip_address, result_list):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }

    url = 'http://ipwhois.cnnic.net.cn/bns/query/Query/ipwhoisQuery.do?txtquery=' + ip_address + '&queryOption=ipv4'
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
        elif count == 4:
            # .encode('latin-1').decode('unicode_escape') 可以解决 str 转换成中文的问题，若是 bytes 则后半部分即可，此处无用
            result_list.append({'单位地址': item.contents[3].text.replace(u'\xa0', '')})
        elif count >= 15 and count < 26:
            result_list.append({item.contents[1].text.split(':')[0] + '-1': item.contents[3].text.replace(u'\xa0', '')})
        elif count >= 26 and count < 36:
            result_list.append({item.contents[1].text.split(':')[0] + '-2': item.contents[3].text.replace(u'\xa0', '')})
        elif count > 36:
            break
        else:
            result_list.append({item.contents[1].text.split(':')[0]: item.contents[3].text.replace(u'\xa0', '')})

    with open('cnnic_ipv4.data', 'wb') as f:
        pickle.dump(result_list, f)

    return result_list


if __name__ == "__main__":
    data_list = []
    data_list = ipv4_data('106.52.89.32', data_list)
