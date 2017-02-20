# coding=utf-8

import functools


def inc(x):
    return x + 1


if __name__ == '__main__':
    items = [1, 2, 3, 4, 5]
    # map() 函数对每个元素执行某一操作
    hander = list(map(inc, items))
    print(hander)
    lambda_hander = list(map(lambda x: x+1, items))
    print(lambda_hander)
    # filter() 函数只抽取函数返回结果为 True 的列表元素
    filter_hander = list(filter((lambda x: x<4), items))
    print(filter_hander)
    # reduce() 函数对列表所有元素依次计算后返回唯一结果，应用必须导入 functools 库
    reduce_hander = functools.reduce((lambda x,y: x/y), items)
    print(reduce_hander)
    # 列表生成式
    s = [x**2 for x in range(6)]
    print(s)
