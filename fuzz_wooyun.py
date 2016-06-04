# coding=utf-8

import urllib.request
from contextlib import closing
import requests
import os
import bs4
import re

file_list = []
dict_list = []
delete_list = ['<a href="?C=N;O=D">Name</a>', '<a href="?C=M;O=A">Last modified</a>',
               '<a href="?C=S;O=A">Size</a>', '<a href="?C=D;O=A">Description</a>',
               '<a href="/">Parent Directory</a>']


def download_file(url, local_filename):
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


def isnotfile(urlname):
    # 如果返回的是-1，即没找到为目录
    back_name = urlname.split('/')[-1]
    if back_name == '':
        return 0
    else:
        return 1


def download_loop(url, download_path):

    # print('这是准备下载的路径:' + url)
    print('这是准备存储的路径:' + download_path)
    print('-------------------------------------')
    content = urllib.request.urlopen(url)
#    data = content.read()
#    data = data.decode('UTF-8')
    result = bs4.BeautifulSoup(content, "html.parser")
    strline = []
    link = result.find_all('a')
# 找到全部a标签
    for line in link:
        strline.append(str(line))
    org_list = strline
    last_list = [x for x in org_list if x not in delete_list]
# 把黑名单洗掉
    for line in last_list:
        if 'Parent Directory' in line:
            last_list.remove(line)
            break
# 单独处理递归进的父目录链接
    strline.clear()
    for correspond in last_list:
        regular = re.compile('<a href="(.*)">(.*)</a>')
        strline.append(regular.split(correspond, 2))
# 目录和名字进行分割
    for over_repeat in strline:
        last_url = str(content.url + over_repeat[1])

        if isnotfile(over_repeat[1]):

            newdir = os.getcwd() + '\\' + over_repeat[2]
            path_exist = os.path.exists(newdir)
            if path_exist:
                print(over_repeat[2] + "已经存在，跳过下载")
            else:
                print('这里应该启动对' + over_repeat[2] + '的下载！')
                local_name = download_file(last_url, over_repeat[2])
                print('已创建文件：' + local_name)

            file_list.append(over_repeat[2])
        else:
            print('这里是' + content.url + '下的' + over_repeat[2])

            if last_url not in dict_list:
                dict_list.append(last_url)

            # newdir = os.getcwd() + '\\' + os.path.normcase(over_repeat[1])
            newdir = os.getcwd() + '\\' + over_repeat[2]
            path_exist = os.path.exists(newdir)

            if not path_exist:
                # print('准备新建的目录名为：' + newdir)
                os.makedirs(newdir)

            os.chdir(newdir)
            download_loop(str(content.url + over_repeat[1]), str(newdir))
            # print('这里的执行路径是：' + os.getcwd())
            os.chdir(os.path.abspath(".."))
            # print('这里的执行路径是：' + os.getcwd())


if __name__ == '__main__':
    # print('请输入你要下载的网站根目录：')
    # print('请输入你要存储的磁盘文件夹：')

    download_loop('http://fuzz.wuyun.org/scanlist/', 'C:\\Users\\Avenger\\Desktop\\wooyun\\')
