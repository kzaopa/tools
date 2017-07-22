#!/usr/bin/env python
#coding:utf-8
#Author:1975

import time

def time_13():
	#上传开始之前运行此脚本，上传完成用户主动中断
	#python 123.py > 111.txt
	tx = ""
	while 1:
		current_milli_time = lambda: int(round(time.time() * 1000))
		#过滤重复的时间戳值
		if not tx == current_milli_time():
			print current_milli_time()
			tx = current_milli_time()
time_13()