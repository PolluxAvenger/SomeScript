# encoding: utf-8

import urllib
import urllib.request
import http.cookiejar

filename = 'C:\\Users\\window\\Desktop\\cookie.txt'
# 声明一个MozillaCookieJar对象实例来保存Cookie，之后写入文件
cookie = http.cookiejar.MozillaCookieJar(filename)

handler = urllib.request.HTTPCookieProcessor(cookie)
# 用这个Cookie生成一个HTTPCookieProcessor，这是一个用来处理Cookie的handler
opener = urllib.request.build_opener(handler)
# 创建一个自定义的opener，把handler传进去
value = {'category': 'xs', 'uid': 'yournumber', 'passwd': 'yourpassword', 'Submit.x': '36', 'Submit.y': '18'}
# 定义表单body字典。submitAuth值是URL编码，编码格式为GB2312，解码以后是进入的意思，不知道为什么会有这样一个奇怪的值
postdata = urllib.parse.urlencode(value).encode(encoding='UTF-8')

# 教学网信息网的URL（用Fiddler捕获分析得到）
loginUrl = 'http://jxxx.ncut.edu.cn/login.asp'
# 模拟登录，并把Cookie保存到变量
result = opener.open(loginUrl, postdata)
# 保存Cookie到cookie.txt中
cookie.save(ignore_discard = True, ignore_expires = True)
# 利用Cookie发出对 必须登录才能访问的 另一个网址的请求，查询绩点是id=6
gradeUrl = 'http://jxxx.ncut.edu.cn/xs/cjkb.asp?id=6'
# 查询成绩是id=5
result = opener.open(gradeUrl)
# 打印出访问到的网页源码
print (result.read())