# coding=utf-8

import re
import urllib
import threading

rawProxyList = []
checkedProxyList = []
targets = []

for i in range(1, 4):
    target = r"http://www.proxy.com.ru/list_%d.html" % i
    targets.append(target)

p = re.compile(b'''<tr><b><td>(\d+)</td><td>(.+?)</td><td>(\d+)</td><td>(.+?)</td><td>(.+?)</td></b></tr>''')


class ProxyGet(threading.Thread):
    def __init__(self, target):
        threading.Thread.__init__(self)
        self.target = target


    def getProxy(self):
        print("代理服务器目标网站： " + self.target)
        req = urllib.request.urlopen(self.target)
        result = req.read()

        try:
            matchs = p.findall(result)
        except Exception as e:
            print(str(e))

        for row in matchs:
            ip = row[1]
            port = row[2]
            addr = row[4].decode("cp936").encode("utf-8")
            proxy = [ip, port, addr]
            rawProxyList.append(proxy)

    def run(self):
        self.getProxy()


if __name__ == "__main__":
    getThreads = []
    checkThreads = []

    for i in range(len(targets)):
        t = ProxyGet(targets[i])
        getThreads.append(t)
    for i in range(len(getThreads)):
        getThreads[i].start()
    for i in range(len(getThreads)):
        getThreads[i].join()

    with open('ip.txt', 'w') as f:
        for item in rawProxyList:
            ip_port = str(item[0].decode('utf-8')) + ':' + str(item[1].decode('utf-8'))
            content = str(item[2].decode('utf-8'))
            result = ip_port + ' ' + content + '\n'
            f.write(str(result))

    print('%s个代理已获得！写入文件成功！' % len(rawProxyList))
