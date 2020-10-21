# -*- coding: utf-8 -*-

"""
@Time : 2019-03-28 14:58
@Author : yangpeng
@File : float_calculte.py
"""

import math


def s(num1):
    if num1 > 127:
        return 1
    return 0


def e(num1, num2):
    e = 0
    num1_list = get_list(num1)
    e_list = num1_list[1:] + [1 if num2 > 127 else 0]

    num = 128
    for s in e_list:
        e += s * num
        num >>= 1

    return e


def get_list(num):
    byte_str = bin(num)[2:]
    byte_str = '0' * (8 - len(byte_str)) + byte_str

    return list(map(int, byte_str))


def x(num2, num3, num4):
    x = 1
    num2_list = get_list(num2)
    m_list = num2_list[1:] + get_list(num3) + get_list(num4)
    i = 2
    for m in m_list:
        x += m / i
        i <<= 1
    return x


def f(s, e, x):
    return math.pow(-1, s) * math.pow(2, e - 127) * x


def get_data(num1, num2, num3, num4):
    return f(s(num1), e(num1, num2), x(num2, num3, num4))


def parse(num1, num2, num3, num4):
    return round(get_data(num1, num2, num3, num4), 2)


def trans(data, nums):
    data = iter(data)
    trans_list = []
    for i in range(nums):
        data_4 = [next(data) for i in range(4)]
        trans_list.append(parse(*data_4[2:], *data_4[:2]))
    return trans_list


def trans2(data, nums):
    data = iter(data)
    trans_list = []
    for i in range(nums):
        data_4 = [next(data) for i in range(4)]
        data_4.reverse()
        trans_list.append(parse(*data_4))
    return trans_list


def trans3(data, nums):
    data = iter(data)
    trans_list = []
    for i in range(nums):
        data_4 = [next(data) for i in range(4)]
        trans_list.append(parse(*data_4))
    return trans_list

