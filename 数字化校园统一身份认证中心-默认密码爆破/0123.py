#!/usr/bin/env python
#coding:utf-8
#data:20170606
import re
#rf = open("6位纯数字.txt", "r")

fileter = re.compile(r"^[0123]")

for n in open("666.txt", "r").readlines():
    if fileter.findall(n):
        with open("03.txt", "a") as w:
            w.write(n)

