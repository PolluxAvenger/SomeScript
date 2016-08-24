#coding=utf-8

import re
import bs4
import urllib.request


def bing_search(keyword, result_list, page_count):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }
    # bing 的搜索很神奇，q 是搜索词，first 是首个的序号，默认每页 10 个结果，可用 count 指定
    page = 1
    while page <= page_count:
        url = 'http://cn.bing.com/search?count=20&q=' + keyword + '&first=' + str(((page-1)*20 + 1))
        request = urllib.request.Request(url, headers=header)
        response = urllib.request.urlopen(request)
        content = response.read()
        result = bs4.BeautifulSoup(content, "html.parser")
        link = result.find_all('h2')

        for item in link:
            url_string = str(item.next)
            regular = re.compile('<a h="(.*)" href="(.*)" (.*)>(.*)</a>')
            match = re.match(regular, url_string)

            try:
                result_list.append(match.group(2))
            except Exception as e:
                # print(e)
                pass

        # print('第' + str(page) + '页一共' + str(len(link)) + '个链接')
        page += 1

    return result_list


if __name__ == '__main__':
    raw_list = []
    result_list = bing_search('12306', raw_list, 5)
