# coding=utf-8

import sys
import json
import time
import requests

API_URL = "https://www.censys.io/api/v1"
API_ID = "your API_ID"
SECRET = "your SECRET"
page = 1
max_page = 3


def getIp(page, keyword):
    iplist = []
    data = {"query": keyword,
            "page": page,
            "fields": ["ip", "protocols", "location.country"]}
    try:
        res = requests.post(API_URL + "/search/ipv4", data=json.dumps(data), auth=(API_ID, SECRET))
        results = res.json()
    except:
        pass

    if res.status_code != 200:
        print("error occurred: %s" % results["error"])
        sys.exit(1)

    iplist.append("Total_count:%s" % (results["metadata"]["count"]))

    for result in results["results"]:
        for i in result["protocols"]:
            iplist.append(result["ip"] + ':' + i + ' in ' + result["location.country"][0])

    return iplist


if __name__ == '__main__':
    while page <= max_page:
        iplist = (getIp(page, 'wordpress'))
        page += 1
        time.sleep(3)

        for item in iplist:
            print(str(item))
