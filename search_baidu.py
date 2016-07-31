# coding=utf-8

import requests
import re
import urllib
import msvcrt
import simplejson
import sys

url = "http://www.baidu.com/s"


def Remove_Repeat(List):  # 列表去重
    New_List = {}.fromkeys(List).keys()
    last_list = list(New_List)

    return last_list


def Split_Url(Url):
    i = 0
    j = 0

    while Url.find("/", i) > 0 and j < 3:
        i = Url.find("/", i) + 1
        j = j + 1

    return Url[:i]


def Get_Url(wd, pn):  # 获取百度搜索的URl

    Url_List = []
    payload = {"wd": wd}

    for i in range(0, pn * 10, 10):
        payload["pn"] = i
        result = requests.get(url, params=payload)
        Url_List = Url_List + re.findall(r"http://www.baidu.com/link\S*(?=\")", result.text)

    return Url_List


def Get_Host(Url_List):  # 获取搜索结果的跟域名
    originalURLs = []

    New_Url_List = Remove_Repeat(Url_List)

    for i in New_Url_List:
        tmpPage = requests.get(i, allow_redirects=False)
        if tmpPage.status_code == 200:
            urlMatch = re.search(b'URL=\'(.*?)\'', tmpPage.text.encode('utf-8'), re.S)
            originalURLs.append((urlMatch.group(1), i))
        elif tmpPage.status_code == 302:
            originalURLs.append((tmpPage.headers.get('location'), i))
        else:
            print('No URL found!!')

    return originalURLs


if __name__ == "__main__":
    temp = Get_Host(Get_Url("12306", 1))  # 搜索关键词与页数
    print('---------------------')
    for i in temp:
        print(i[0])
