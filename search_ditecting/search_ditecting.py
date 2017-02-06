# coding=utf-8

import bs4
import urllib
import urllib.request


def search_ditecting(keyword):
    'keyword%3ASiemens '
    word = urllib.parse.unquote(keyword)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
        'Referer': 'http://icsfind.com/index.php/home/Index/index'
    }

    url = 'http://icsfind.com/index.php/home/Index/index/index.php/home/result/index.html?query=' + word
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    content = response.read()
    result = bs4.BeautifulSoup(content, "html.parser")
    link = result.find_all('p', {'class': "show"})

    for item in link:
        print(item.get_text())


if __name__ == '__main__':
    search_ditecting('keyword Siemens')
