# coding=utf-8

from bs4 import BeautifulSoup
from io import StringIO
from io import BytesIO
import urllib.request
import socket
import random
import types
import time
import gzip
import sys
import re

base_url = 'https://www.google.com.hk/'
results_per_page = 10

user_agents = list()

# 从搜索引擎返回的结果
class SearchResult:
    def __init__(self):
        self.url= '' 
        self.title = '' 
        self.content = '' 

    def getURL(self):
        return self.url

    def setURL(self, url):
        self.url = url 

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content

    def printIt(self, prefix = ''):
        print('url\t->', self.url)
        print('title\t->', self.title)
        print('content\t->', self.content)

    def writeFile(self, filename):
        file = open(filename, 'a')
        try:
            file.write('url:' + self.url+ '\n')
            file.write('title:' + self.title + '\n')
            file.write('content:' + self.content + '\n\n')

        except IOError as e:
            print('file error:', e)
        finally:
            file.close()


class GoogleAPI:
    def __init__(self):
        timeout = 40
        socket.setdefaulttimeout(timeout)

    def randomSleep(self):
        sleeptime =  random.randint(60, 120)
        time.sleep(sleeptime)

    #从 URL 里提取域名
    def extractDomain(self, url):
        domain = ''
        pattern = re.compile(r'http[s]?://([^/]+)/', re.U | re.M)
        url_match = pattern.search(url)
        if(url_match and url_match.lastindex > 0):
            domain = url_match.group(1)

        return domain

    #从链接中提取 URL
    def extractUrl(self, href):
        url = ''
        pattern = re.compile(r'(http[s]?://[^&]+)&', re.U | re.M)
        url_match = pattern.search(href)
        if(url_match and url_match.lastindex > 0):
            url = url_match.group(1)

        return url 

    # 从得到的 HTML 文件中提取搜索引擎结果列表
    def extractSearchResults(self, html):
        results = list()
        soup = BeautifulSoup(html, "html.parser")
        lis = soup.find_all('h3', 'r')

        if(len(lis) > 0):
            for li in lis:
                result = SearchResult()

                link = li.find('a')
                url = str(link)
                url = self.extractUrl(url)
                #此处应该判断 URL 是否为空，如果是空就进入下一轮
                title = link.renderContents()

                result.setURL(url)
                result.setTitle(title)
                result.setContent('')

                results.append(result)
        else:
            print('一个都没匹配到！')

        return results


    # @param query -> 搜索的关键字
    # @param lang -> 搜索的语言
    # @param num -> 搜索结果返回的数量
    def search(self, query, lang='en', num=results_per_page):
        search_results = list()
        query = urllib.request.quote(query)

        if(num % results_per_page == 0):
            pages = num / results_per_page
        else:
            pages = num / results_per_page + 1

        pages = int(pages)

        for p in range(0, pages):
            start = p * results_per_page 
            url = '%s/search?hl=%s&num=%d&start=%s&q=%s' % (base_url, lang, results_per_page, start, query)
            retry = 3
            while(retry > 0):
                try:
                    request = urllib.request.Request(url)
                    length = len(user_agents)
                    index = random.randint(0, length-1)

                    user_agent = user_agents[index] 
                    request.add_header('User-agent', user_agent)
                    request.add_header('connection','keep-alive')
                    request.add_header('Accept-Encoding', 'gzip')
                    request.add_header('referer', base_url)

                    response = urllib.request.urlopen(request)
                    html = response.read()

                    if(response.headers.get('content-encoding', None) == 'gzip'):
                        html = gzip.GzipFile(fileobj=BytesIO(html)).read()

                    results = self.extractSearchResults(html)
                    search_results.extend(results)
                    break
                except urllib.request.URLError as e:
                    print('url error:', e)
                    self.randomSleep()
                    retry = retry - 1
                    continue
                
                except Exception as e:
                    print('error:', e)
                    retry = retry - 1
                    self.randomSleep()
                    continue

        return search_results 


def load_user_agent():
    fp = open('./user_agents', 'r')

    line  = fp.readline().strip('\n')

    while(line):
        user_agents.append(line)
        line = fp.readline().strip('\n')

    fp.close()


def crawler():
    # 从文件中加载 UA 来使用
    load_user_agent()
    # 创建一个实例
    api = GoogleAPI()
    # 设定搜索结果数量
    expect_num = 10
    # 如果没有设定参数，就从 keywords 中读取
    if(len(sys.argv) < 2):
        keywords = open('./keywords', 'r')
        keyword = keywords.readline()

        while(keyword):
            results = api.search(keyword, num = expect_num)
            for r in results:
                r.printIt()
            keyword = keywords.readline()
        keywords.close()
    else:
        keyword = sys.argv[1]
        results = api.search(keyword, num = expect_num)

        for r in results:
            r.printIt()

if __name__ == '__main__':
    crawler()
