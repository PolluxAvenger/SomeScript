# coding=utf-8


import time
import hashlib
import urllib.parse
import urllib.request


def extract_data(url, data_length, word='中国'):
    data = {}
    data['i'] = word
    data['from'] = 'zh-CHS'
    data['to'] = 'en'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['salt'] = '1498183775133'
    data['sign'] = 'd42894899a91acfab33a48060789ccdf'
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_ENTER'
    data['typoResult'] = 'true'

    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': data_length,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=aaaPI1eG0FF9E6yinmqZv; SESSION_FROM_COOKIE=fanyiweb; OUTFOX_SEARCH_USER_ID=1081847622@10.169.0.21; _ntes_nnid=0f7883df5925c4016452497487563d52,1498141479802; OUTFOX_SEARCH_USER_ID_NCOO=900639528.7607046; ___rl__test__cookies=1498183775128',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    request = urllib.request.Request(url, headers=header, data=urllib.parse.urlencode(data).encode('utf-8'))
    response = urllib.request.urlopen(request)
    content = response.read()
    print(content)


if __name__ == '__main__':

    print(time.strptime("1493126127995", '%Y-%m-%d %H:%M:%S'))


    word = '美国'
    word_url = urllib.parse.quote(word)
    length = 198 + len(word_url)

    unix_time = '1498183775133'
    result_word = unix_time
    m = hashlib.md5()
    m.update(result_word.encode(encoding="utf-8"))
    print(m.hexdigest())


    extract_data('http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom=null', length, word)
    print('--------')
