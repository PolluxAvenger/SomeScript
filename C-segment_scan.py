# coding=utf-8

import nmap
import json
import socket
import requests
from concurrent.futures import ThreadPoolExecutor


def worker(ip_address):
    global result_list

    print('正在搜索' + ip_address)

    try:
        nmap_Scan = nmap.PortScanner()
        nmap_Scan.scan(ip_address, '22-443')
    except Exception as e:
        print(str(e))

    for host in nmap_Scan.all_hosts():
        port_info = []

        for protocol in nmap_Scan[host].all_protocols():
            try:
                lport = nmap_Scan[host][protocol].keys()
            except Exception as e:
                print(str(e))
                continue

            for port in lport:
                try:
                    port_info.append({'port': port, 'status': nmap_Scan[host][protocol][port]['state']})
                except Exception as e:
                    print(str(e))
        # 还缺少一个对 port_info 是否为空的判断，为空就不写入了
        try:
            result = {ip_address: port_info}
        except Exception as e:
            print(str(e))

    print(ip_address + '完成搜索')
    result_list.append(result)
    print(ip_address + '写入结果完毕')


def http_alive(ip_address):
    global result_list

    for port in [80, 443, 8080]:
       link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       link.settimeout(2)
       status = link.connect_ex((str(ip_address), int(port)))

       if status == 0:
           result_list.append(str(ip_address + ':' + str(port)))

		   
def long_data(data):
    with open('port.json', 'w') as f:
        json.dump(data, f, indent=4)


def ip2domain():
    # 准备从 http://ip.aa2.cn 获得域名信息
    print('B')


if __name__ == '__main__':
    result_list = []

    r = requests.get('http://ipinfo.io')
    result = r.json()
    ip_address = result['ip'].split('.')
    net_address = '.'.join(ip_address[:-1])

    # net_address = '123.58.180' # 网易验证 180.149.134.141 新浪验证

    with ThreadPoolExecutor(max_workers=10) as executor:
        for item in range(8, 10):
            ip = '%s.%s' % (net_address, item)
            executor.submit(worker, ip)

    long_data(result_list)
