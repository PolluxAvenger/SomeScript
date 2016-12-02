# coding=utf-8

import os
import csv
import pickle
import datetime
import requests
from concurrent.futures import ThreadPoolExecutor


def download_file(url, file_name):
    r = requests.get(url, stream=True)
    file_type = file_name.split('.')[0]
    local_name = os.path.join(os.getcwd(), 'data', (file_type + '_ip.data'))
    ip_list = []

    os.makedirs(os.path.dirname(local_name), exist_ok=True)

    with open((file_type + '_row.txt'), "wb") as t:
        t.write(r.content)

    with open((file_type + '_row.txt'), "rb") as x:
        for item in x:
            ip_list.append({'Type': file_type, 'IP': item.decode().split('\n')[0]})

    os.remove(file_type + '_row.txt')

    with open(local_name, 'wb') as f:
        pickle.dump(ip_list, f)

    return local_name


def csv_write(filename, ip_list):
    with open(filename, 'w') as f:
        headers=['Type', 'IP']
        writer = csv.DictWriter(f, headers)
        writer.writeheader()

        for item in ip_list:
            writer.writerow(item)


def data_extract(local_name):
    with open(local_name, 'rb') as f:
        data_list = pickle.load(f)

    return data_list


def worker(url):
    file_name = os.path.basename(url)
    ip_type = file_name.split('.')[0]
    csv_name = ip_type + '_ip_' + str(datetime.date.today()) + '.csv'
    csv_file = os.path.join(os.getcwd(), 'csv', csv_name)
    data_file = download_file(url, file_name)
    ip_list = data_extract(data_file)
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    csv_write(csv_file, ip_list)
    print('写入了' + str(len(ip_list)) + '个' + str(ip_type) + '型的恶意 IP 地址写到' + str(csv_name) + '中!')


if __name__ == '__main__':
    url_list = ['https://lists.blocklist.de/lists/ssh.txt',
                'https://lists.blocklist.de/lists/mail.txt',
                'https://lists.blocklist.de/lists/apache.txt',
                'https://lists.blocklist.de/lists/imap.txt',
                'https://lists.blocklist.de/lists/ftp.txt',
                'https://lists.blocklist.de/lists/sip.txt',
                'https://lists.blocklist.de/lists/bots.txt',
                'https://lists.blocklist.de/lists/strongips.txt',
                'https://lists.blocklist.de/lists/ircbot.txt',
                'https://lists.blocklist.de/lists/bruteforcelogin.txt']

    with ThreadPoolExecutor(max_workers=5) as executor:
        for url in url_list:
            executor.submit(worker, url)
