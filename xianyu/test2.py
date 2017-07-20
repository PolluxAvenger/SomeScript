# coding=utf-8

import bs4
import csv
import time
import random
import urllib.request
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor


result_list = []


def worker(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }

    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    content = response.read()
    result = bs4.BeautifulSoup(content, "html.parser")
    link = result.find_all('li', {'class': "item-info-wrapper item-idle clearfix"})

    for item in link:
        goods = item.contents[1]
        saler = item.contents[3]

        result_list.append({
            'URL': 'https:' + goods.contents[3].contents[0].attrs['href'],
            'Title': goods.contents[3].text,
            'Price': goods.contents[5].text,
            'Describe': goods.contents[7].text,
            'Name': saler.contents[1].contents[3].text.strip(),
            'Location': saler.contents[1].contents[5].text,
            'Level': saler.contents[1].contents[7].text.strip()
        })

    time.sleep(random.randint(8, 15))


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        for item in range(1, 21):
            url = 'https://s.2.taobao.com/list/list.htm?st_edtime=1&page=' + str(item) + '&ist=0&q=%s' % (quote('小米六'.encode('gbk')))
            executor.submit(worker, url)

    with open('data.csv', 'w', newline='', encoding='utf-8') as t:
        headers = ['URL', 'Title', 'Price', 'Describe', 'Name', 'Location', 'Level']
        writer = csv.DictWriter(t, headers)
        writer.writeheader()

        for item in result_list:
            writer.writerow(item)
