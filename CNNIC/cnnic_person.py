# coding=utf-8

import bs4
import pickle
import urllib.request


def person_data(person_info, result_list):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }

    url = 'http://ipwhois.cnnic.net.cn/bns/query/Query/ipwhoisQuery.do?txtquery=' + person_info + '&queryOption=person'
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
        elif count <= 11:
            result_list.append({item.contents[1].text.split(':')[0] : item.contents[3].text.replace(u'\xa0', '')})
        elif count >= 13 and count < 23:
            result_list.append({item.contents[1].text.split(':')[0] : item.contents[3].text.replace(u'\xa0', '')})
        elif count > 23:
            break
        else:
            result_list.append({item.contents[1].text.split(':')[0]: item.contents[3].text.replace(u'\xa0', '')})

    with open('cnnic_person.data', 'wb') as f:
        pickle.dump(result_list, f)

    return result_list


if __name__ == "__main__":
    data_list = []
    data_list = person_data('IPAS1-CN', data_list)
