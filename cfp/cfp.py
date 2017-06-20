# coding=utf-8

import json
import pickle
import urllib.request


if __name__ == "__main__":
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }

    url = 'https://cfptime.org/cfps/json'
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    content = response.read()
    result = json.loads(content.decode())
    print(result)

    with open('cfp_time.data', 'wb') as f:
        pickle.dump(result, f)
