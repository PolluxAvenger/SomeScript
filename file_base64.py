# coding=utf-8

import base64


if __name__=="__main__":
    result_list = []

    with open('in.txt', 'rb') as in_file:
        with open('result.txt', 'w') as out_file:
            for item in in_file:
                out_file.write(base64.b64encode(item).decode() + '\n')
