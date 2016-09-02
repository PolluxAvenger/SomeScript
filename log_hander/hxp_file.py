# coding=utf-8

import os
import shutil

def file_clean(dir_path = 'C:\\Users\\window\\Desktop\\ip_hander\\test'):
    result = []

    exist = os.path.exists(dir_path)

    for root, dirname, filename in os.walk(dir_path):
        for eachfile in filename:
            if os.path.getsize(dir_path + '\\' + eachfile) > 0:
                result.append(eachfile)

    if exist:
        test = os.listdir(dir_path)
        length = len(test)

        if length > 0:
            shutil.rmtree(dir_path)
            print('已经删掉了！')
            os.mkdir("test")
            print('创建完成！')
    else:
        os.mkdir("test")

    with open(dir_path + '\\' + 'result.txt', 'a+') as f:
        for item in result:
            f.write(item + '\n')


def dir_clean(dir_path = 'C:\\Users\\window\\Desktop\\ip_hander\\test'):
    exist = os.path.exists(dir_path)

    if exist:
        test = os.listdir(dir_path)
        length = len(test)

        if length > 0:
            shutil.rmtree(dir_path)
            print('已经删掉了！')
            os.mkdir("test")
            print('创建完成！')
    else:
        os.mkdir("test")


file_clean()
