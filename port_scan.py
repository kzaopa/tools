#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#Author: 1975
#date: 20170227
import socket,sys

'''
简易端口扫描脚本
'''

ports=[80,81,82,83,84,85,86,87,88,89,9090,1099,8000,443,873,5984,6379,7001,7002,9200,9300,11211,27017,27018,50000,50060,50070,50030,2375,3128,2601,2604,4440,4848,9000,9043,21,22,23,161,389,445,1433,1521,3306,3389,5432,5900]
host=sys.argv[1]
for port in ports:
  try:
    print "[+] Attempting to connect to "+host+":"+str(port)
    s=socket.socket()
    s.connect((host,port))
    s.send('port connect \n')
    banner=s.recv(10)
    if banner:
      print "[+] Port "+str(port)+" open"
    s.close()
  except: pass
