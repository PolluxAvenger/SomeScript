# coding=utf-8
# 'http://www.malwaredomainlist.com/mdlcsv.php'

import csv
import pickle


def dga_data():
    result_list = []

    with open('dga.txt', 'rb') as d:
        all_line = d.readlines()
        for line in all_line:
            result = line.decode().split('\t')
            result_list.append({'Family': result[0], 'Domain': result[1]})

    with open('dga_track_360_12-23.data', 'wb') as f:
        pickle.dump(result_list, f)

    print(str(len(result_list)))
    # 解决 Windows 系统下多余空行的问题
    with open('dga_track_360_12-23.csv', 'w', newline='') as t:
        headers = ['Family', 'Domain']
        writer = csv.DictWriter(t, headers)
        writer.writeheader()

        for item in result_list:
            try:
                writer.writerow(item)
            except Exception as e:
                continue


if __name__ == '__main__':
    dga_data()
