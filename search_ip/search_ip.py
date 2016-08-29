# coding=utf-8

import bs4
import urllib.request


def search_ip(domain):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
        'Referer': 'http://ip.chinaz.com/'
    }

    url = 'http://ip.chinaz.com/?ip=' + domain
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    content = response.read()
    result = bs4.BeautifulSoup(content, "html.parser")
    link = result.find_all('p', {'class': "WhwtdWrap bor-b1s col-gray03"})

    with open('re_ip.txt', 'w') as f:
        for item in link:
            f.write(item.text)


if __name__ == '__main__':
    search_ip('qq.com')
