# coding=utf-8

import re
import json


lines = ""
data_regular = re.compile('[0-9]{8}\-.+')
title_regular = re.compile('\[.{5,}\]')
dict_t = {}


def read_txt(path):
    name = ''

    with open(path, 'r', encoding='gbk') as f:
        date_flag = True
        title_flag = True
        tag_flag = True
        url_flag = True

        for item in f:
            item = item.strip().replace('【', '[')
            item = item.strip().replace('】', ']')
            date_match = re.match(data_regular, item)
            title_match = re.match(title_regular, item)

            if date_match == None and title_match == None and title_flag:
                continue
            elif date_flag:
                name = date_match.string.strip()
                dict_t[name] = {}
                dict_t[name]['Date'] = date_match.string.strip().split('-')[0]
                date_flag = False
                continue

            if title_flag:
                dict_t[name]['Title'] = item.split(']')[0].split('[')[1]
                dict_t[name]['Content'] = item.split(']')[1].strip()
                title_flag = False
                continue

            if tag_flag:
                tag_list = item.split(': ')[1].split('; ')
                tag_list = [item.strip() for item in tag_list]
                dict_t[name]['Tag'] = tag_list
                tag_flag = False
                continue

            if url_flag:
                dict_t[name]['URL'] = item.split('URL: ')[1]
                date_flag = True
                title_flag = True
                tag_flag = True
                continue


if __name__ == "__main__":
    paths = 'inform.txt'
    read_txt(paths)
    result = json.dumps(dict_t, indent=4, ensure_ascii=False)

    with open('test.json', 'w', encoding='utf-8') as t:
        t.write(result)
