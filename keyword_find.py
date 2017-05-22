#!/usr/bin/env python
#coding:utf-8
#Date:20170518
#Author:1975

import Queue
import threading
import sys
import urllib2
from time import ctime
#from bs4 import BeautifulSoup

lock = threading.Lock()
keyword = 'OPAC v'   #判断关键字

def http_request():

    print '***' +str(threading.active_count())+ '***--enumerate'
    while True:
        host = queue.get()
        if host == 'quit':
            break

        host = host + '/opac/search.php'

        try:
            request = urllib2.Request(host)
            respone = urllib2.urlopen(request, timeout=5)
            data = respone.read()
        except:
            data = ""
        
        if not len(data) > 0:
            continue
        if keyword in data:
            lock.acquire()
            #print '[*]:find vulnerable host', host
            with open('vul_hosts.txt', 'a') as outFile:
                outFile.write(host+'\n')
            lock.release()
        else:
            print host


if __name__ == '__main__':
    print '[*] start time:', ctime()
    queue = Queue.Queue()
    threads = []
    try:
        m = int(sys.argv[2])
    except:
        m = 100
    for h in open(sys.argv[1], 'r').readlines():
        h = h.strip()
        queue.put(h)
    
    for i in range(m):
        t = threading.Thread(target=http_request)
        threads.append(t)
        t.start()

    for b in threads:
        queue.put('quit')

    for t in threads:
        t.join()
    
    print '[+] hosts scanned all Done. end time:', ctime()
