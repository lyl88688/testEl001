

#!/usr/bin/env python
# coding=utf-8
from timeit import timeit

def login():
    print("登录")

def test_1():
    print('测试用例1')

def test_2():
    print('测试用例2')


def test_unchangeable_tuple():
    list = [1,4,7]
    list2 = [1,4,7]
    print('list 的内存地址：',id(list))
    print('list2 的内存地址：',id(list2))
    list2[1] = 3
    print('修改后的list2 ',list2)
    print('修改后的list2 的内存地址：',id(list2))
    tuple = (1, 2, 3, [1, 4, 7])
    print('修改前的tuple：',tuple)
    print('修改前的tuple内存地址：',id(tuple))
    tuple[3][2] = 100
    print('修改后的tuple：',tuple)
    print('修改后的tuple内存地址：',id(tuple))


if __name__ == '__main__':
    pass