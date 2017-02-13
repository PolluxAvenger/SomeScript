# coding=utf-8

import re
import os
import csv
import requests


def extract_data(url):
    file_name = os.path.basename(url)
    r = requests.get(url, stream=True)
    file_type = file_name.split('.')[0]
    local_name = os.path.join(os.getcwd(), 'dga', (file_type + '.data'))
    ip_list = []
    os.makedirs(os.path.dirname(local_name), exist_ok=True)

    with open((file_type + '_row.txt'), "wb") as t:
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                t.write(chunk)

    with open((file_type + '_row.txt'), "rb") as x:
        count = 0
        for item in x:
            if count < 14:
                count += 1
                continue

            split_result = str(item).split(',')
            regular = re.compile(r'Domain used by \b(.+?) \b')
            family = re.match(regular, split_result[1])

            ip_list.append({'Domain': split_result[0],
                            'Date': split_result[2],
                            'Family': family.group(1).split(' ')[0]})

    os.remove(file_type + '_row.txt')

    with open('dga_all_track.csv', 'w', newline='', encoding='utf-8') as t:
        headers = ['Domain', 'Date', 'Family']
        writer = csv.DictWriter(t, headers)
        writer.writeheader()

        for item in ip_list:
            writer.writerow(item)


if __name__ == '__main__':
    extract_data('http://osint.bambenekconsulting.com/feeds/dga-feed.txt')
