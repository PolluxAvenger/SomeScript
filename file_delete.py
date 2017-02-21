# coding = utf-8

import os


def file_clean(dir_path = 'C:\\'):
    for root, dirname, filename in os.walk(dir_path):
        for eachfile in filename:
            if eachfile == 'Thumbs.db':
                print('Thumbs.db Delete!')
                file_path = root + '\\' + eachfile
                print(file_path)
                os.remove(file_path)
            else:
                continue

        for item in dirname:
            path = root + item
            file_clean(path)


dir_list = ['C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\']
for item in dir_list:
    try:
        file_clean(item)
        print('进入了' + item)
    except Exception as e:
        print('错啦！')
        pass
