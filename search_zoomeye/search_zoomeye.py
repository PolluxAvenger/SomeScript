# coding=utf-8

import json
import requests


def ZoomEye_Login(strUsername='yourusername', strPasswd='yourpassword'):
    strZoomEyeLoginUrl = 'https://api.zoomeye.org/user/login'
    data = {
        'username': strUsername,
        'password': strPasswd
    }
    json_data = json.dumps(data)
    data_encoded = json_data.encode('utf-8')
    req = requests.post(url=strZoomEyeLoginUrl, data=data_encoded)
    return req.json()['access_token']


def apiTest(access_token, keyword='wordpress', page = 1, maxpage = 10):
    headers = {'Authorization': access_token,}

    while (True):
        try:
            r = requests.get(url='http://api.zoomeye.org/host/search?query="' + keyword + '"' + str(page), headers=headers)
            r_decoded = json.loads(r.text)
            print(r_decoded)
        except Exception as e:
            print(str(e))

        if page == maxpage:
            break
        page += 1


if __name__ == '__main__':
    LoginToken = ZoomEye_Login()
    strLoginToken = "JWT " + LoginToken
    apiTest(strLoginToken)
