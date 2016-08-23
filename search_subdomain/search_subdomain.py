#coding=utf-8

import re
import bs4
import urllib.request


def domain_title(domain_list):
    title_list = []
    header = {
        'Referer': 'https://www.google.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
    }

    for item in domain_list:
        if 'http://' not in item:
            url = 'http://' + item
            if 'http://.' in url:
                url = 'http://' + item.lstrip('.')
        if '.http://' in item:
            url = item.lstrip('.')

        try:
            request = urllib.request.Request(url, headers=header)
            response = urllib.request.urlopen(request)
            content = response.read()
            result = bs4.BeautifulSoup(content, "html.parser", from_encoding="GBK")
            link = result.find_all('title')
            title_list.append((url, link[0].text))
            # print(url + '-----' + link[0].text)

        except Exception as e:
            title_list.append((url, None))
            # print('错误是：' + str(e))
            pass

    return title_list


def links_get_domain(domain, result_list):
    headers = \
    {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "http://i.links.cn/subdomain/",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }

    value = {"domain": domain, "b2": '1', "b3": '1', "b4": '1', "": '%B2%E9+%D1%AF'}
    data = urllib.parse.urlencode(value).encode('utf-8')
    url = 'http://i.links.cn/subdomain/'

    request = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(request)
    content = response.read()

    result = bs4.BeautifulSoup(content, "html.parser")
    link = result.find_all('div', {'class': 'domain'})

    for item in link:
        subdomain = re.split('(\d).(.*)', item.text)
        result_list.append(subdomain[2])

    return result_list


if __name__ == '__main__':
    white_list = []
    links_subdomain_list = links_get_domain('qq.com', white_list)
    print('links 得到了' + str(len(links_subdomain_list)) + '个子域名！')
    print(links_subdomain_list)
    title_list = domain_title(links_subdomain_list)
    print(title_list)
