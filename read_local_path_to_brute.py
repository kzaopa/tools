#!/usr/lib/env python
#coding:utf-8
#data:20170604
#Author:python黑帽子 p73-74

import Queue
import threading
import os
import urllib2
import sys

try:
    m = int(sys.argv[3])
except:
    m = 30

try:
    target = sys.argv[1]
except:
    print 'usage: test.py 127.0.0.1 /roo/filepath 30'
    print 'option the number of threads, default 30'
    sys.exit()

try:
    directory = sys.argv[2]
except:
    print 'usage: test.py 127.0.0.1 /roo/filepath 30'
    print 'option the number of threads, default 30'
    sys.exit()

filters = ['.jpg', '.png', '.gif', '.css']

os.chdir(directory)
web_paths = Queue.Queue()

for r,d,f in os.walk('.'):
    for files in f:
        remote_path = "%s/%s" % (r, files)
        if remote_path.startswith('.'):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path.replace('\\', '/'))
    for dirs in d:
        remote_dir = "%s/%s" % (r, dirs)
        if remote_dir.startswith('.'):
            remote_dir = remote_dir[1:]
        web_paths.put(remote_dir.replace('\\', '/'))

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        if path == 'quit':
            break
        url = "%s%s" % (target, path)
        request = urllib2.Request(url)
        try:
            respone = urllib2.urlopen(request)
            content = respone.read()
            print "[%d] => %s" % (respone.code, path)
            with open('exists.txt', 'a') as w:
                w.write(url+'\n')
            respone.close()
        except urllib2.HTTPError as error:
            #print "Faild %s" % error.code
            pass

if __name__ == '__main__' :
    threads = []

    for i in range(m):
        t = threading.Thread(target=test_remote)
        threads.append(t)
        t.start()

    for q in threads:
        web_paths.put('quit')

    for t in threads:
        t.join()
    print '[+] all directory scanned Done.'