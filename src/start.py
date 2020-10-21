#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mm
# @Date  : 2020-10-21
# import lib
# !/usr/bin/env python3
# coding=utf-8

import argparse
import os
import subprocess
main_path = os.path.join(os.path.dirname(__file__), 'TCP.py')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='开始接收数据')
    parser.add_argument('-p', '--port', type=int, nargs="+", help='Port of TCP')
    args = parser.parse_args()
    if args.port:
        for port in args.port:
            subprocess.Popen('nohup python3 {} -p {} >/dev/null 2>&1 &'.format(main_path, port), shell=True)
