#!/usr/bin/env python
#coding:utf-8
#data:20170606
'''
usage: test.py 4
usage: test.py 6
'''

import sys
import random

number = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
string = 'abcdefghjklmnopqrst'

try:
    length = int(sys.argv[1])
except:
    length = 0

n = ""
l = random.sample(string, length)

def num(length, l):
    global n
    length -= 1
    if not (length < 0):
        for l[length] in number:
            #print l[length]
            num(length, l)
    else:
        #n = str(l[0])+str(l[1])+str(l[2])+str(l[3])+str(l[4])+str(l[5])
        n = str(l[0])+str(l[1])+str(l[2])+str(l[3])
        print n

num(length, l)