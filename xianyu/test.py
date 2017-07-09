# coding=utf-8

import time
from pyquery import PyQuery
from urllib.parse import urlparse, parse_qs, quote


keywords = ['一加五', '小米六']


def get_url(keyword):
    url = 'https://s.2.taobao.com/list/list.htm?st_edtime=1&ist=0&q=%s' % (quote(keyword.encode('gbk')))
    return url


def process(url):
    doc = PyQuery(url)
    item_info_list = doc('ul li div.item-info')
    for item_info in item_info_list:
        item_info = doc('ul li div.item-info').eq(0)
        item_url = item_info('div.item-pic a').attr('href')
        r = urlparse(item_url)
        item_id = parse_qs(r.query)['id'][0]
        item_title = item_info('h4.item-title').text()
        item_price = item_info('div.item-price span.price em').text()
        item_description = item_info('div.item-description').text()
        item_url = item_info('div.item-pic a').attr('href')
        msg = "%s \n%s \n%s \nhttps:%s" % (item_title, item_price, item_description, item_url)
        print(msg)


if __name__ == '__main__':
    while 1:
        for keyword in keywords:
            url = get_url(keyword)
            process(url)
        time.sleep(10)
