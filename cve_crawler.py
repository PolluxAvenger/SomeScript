# coding=utf-8

import csv
import bs4
import time
import pickle
import requests


def cve_data(result_list, cvssscoremin=9, cvssscoremax=10):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }
    page = 1

    while page < 30:
        url = 'http://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=' + str(page) + '&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=' + str(cvssscoremin) + '&cvssscoremax=' + str(cvssscoremax) +'&year=0&month=0&cweid=0&order=1&trc=12557&sha=c560d509f935c26128bfb13d2f2dadfcea62215b'
        response = requests.get(url, headers=header)
        result = bs4.BeautifulSoup(response.text, "lxml")

        for item in result.find_all("tr", {'class': "srrowns"}):
            item_list = []
            for ilem in item.find_all('td'):
                ilem_sult = ilem.text.encode('utf-8').strip()
                if  ilem_sult != ' ':
                    item_list.append(ilem_sult.decode())

            result_list.append({'Number': item_list[0],
                                'CVE ID': item_list[1],
                                'CWE ID': item_list[2],
                                'Exploits': item_list[3],
                                'Vulnerability Type': item_list[4],
                                'Publish Date': item_list[5],
                                'Update Date': item_list[6],
                                'Score': item_list[7],
                                'Gained Access Level': item_list[8],
                                'Access': item_list[9],
                                'Complexity': item_list[10],
                                'Authentication': item_list[11],
                                'Conf': item_list[12],
                                'Integ': item_list[13],
                                'Avail': item_list[14]})

        page += 1
        time.sleep(3)

    with open('cve_list.data', 'wb') as f:
        pickle.dump(result_list, f)

    return result_list


def extract():
    with open('cve_list.data', 'rb') as f:
        data_list = pickle.load(f)

    print('抽取完毕！共抽出' + str(len(data_list)) +'个数据行.')

    with open('cve_list.csv', 'w', newline='', encoding='utf-8') as t:
        headers = ['Number', 'CVE ID', 'CWE ID', 'Exploits', 'Vulnerability Type', 'Publish Date', 'Update Date',
                   'Score', 'Gained Access Level', 'Access', 'Complexity', 'Authentication', 'Conf', 'Integ', 'Avail']

        writer = csv.DictWriter(t, headers)
        writer.writeheader()

        for item in data_list:
            writer.writerow(item)


if __name__ == "__main__":
    cve_data_list = []
    'http://www.cvedetails.com/cve/CVE-2017-8890/ 漏洞详情'
    cve_data_list = cve_data(cve_data_list)
    extract()
