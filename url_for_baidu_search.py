#!/usr/bin/env python
#coding:utf-8
#Date:20170517
#Author:1975

import Queue
import threading
import sys
import urllib2
import random
from time import ctime
from bs4 import BeautifulSoup

'''
useg: python test.py keyword [option pages, default 10]
example: python test.py site:edu.cn 70
'''

lock = threading.Lock()
user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
    (KHTML, like Gecko) Element Browser 5.0',
    'IBM WebExplorer /v0.94',
    'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
    Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/28.0.1468.0 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

def http_req():
    while True:
        try:
            url = queue.get(timeout=0.1)
        except:
            break
        try:
            r = random.randint(0, 9)
            ua = {'User-Agent':user_agents[r]}
            request = urllib2.Request(url, headers=ua)
            respone = urllib2.urlopen(request, timeout=7)
            data = respone.read()
        except:
            data = ""
        
        if not len(data) > 0:
            break
        data_soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        urls = data_soup.find_all('div', class_='f13')
        _urls = [u.get_text().split('-')[0] for u in urls]
        for s in _urls:
            lock.acquire()
            s = s.split('/')[0]
            url_list.append(s)
            lock.release()

if __name__ == '__main__':
    print 'start time:', ctime()
    try:
        keys = sys.argv[1]
    except:
        print 'usage: test.py keywords (options:page, default page=10)'
        sys.exit(0)
    try:
        page = int(sys.argv[2])
    except:
        page = 10
    queue = Queue.Queue()
    for p in xrange(1, page+1):
        host = 'http://www.baidu.com/s?wd=%s&pn=%s' % (keys, p*9)
        queue.put(host)
    threads = []
    url_list = []
    for t in range(70):
        t = threading.Thread(target=http_req)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    url_list = [l for l in set(url_list) if len(l) > 8]
    for x in url_list:
        print x
    print len(url_list)
    print 'end time:', ctime()