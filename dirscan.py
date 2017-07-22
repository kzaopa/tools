#!/usr/lib/env python
#coding:utf-8
#data:20170604
#Author:python黑帽子 p76-79

import os
import Queue
import threading
import sys
import requests
import random
from datetime import datetime

threads = []
words = Queue.Queue()
try:
    m = int(sys.argv[3])
except:
    m = 30

try:
    target = sys.argv[1]
except:
    print 'usage: dirscan.py url dict_file (option: multithreading, default m=30)'
    sys.exit(0)

try:
    wordlist_file = sys.argv[2]
except:
    print 'usage: dirscan.py url dict_file (option: m(multithreading) ,default m=30)'
    sys.exit(0)

resume = None
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"

def build_wordlist(wordlist_file):
    global words
    #读入字典文件
    fd = open(wordlist_file, "rb")
    raw_words = fd.readlines()
    fd.close()
    found_resume = False
    for word in raw_words:
        word = word.rstrip()
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print "Resuming wordlist from: %s" % resume
        else:
            words.put(word)
    return words

def dir_bruter(word_queue, extensions=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        if attempt == 'quit':
            break
        attempt_list = []

        #检查是否有文件扩展名，如果没有就是我们要暴力破解的路径
        if "." not in attempt:
            attempt_list.append("%s/" % attempt)
        else:
            attempt_list.append("%s" % attempt)

        #如果我们想暴力扩展
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt, extension))

        #迭代我们要尝试的文件列表
        for brute in attempt_list:
            url = "%s%s" % (target, brute)
            try:
                headers = {}
                results = {}
                headers["User-Agent"] = user_agent
                respone = requests.get(url, headers=headers)
                if len(respone.text):
                    code = respone.status_code
                    results['status_code'] = str(code)
                    results['url'] = url
                    if code == 200 or code == 403 or code == 500 or code ==400:
                        saveResult(filename, results)
                        print "[%d] => %s" % (code, url)
            except:
                pass
                #print "!!! %d => %s" % (code, url)
                
def saveHead(filename):
    head = '''
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <title>DirScan</title>
                    <link rel="stylesheet" href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css"> 
                    <link rel="stylesheet" href="http://cdn.bootcss.com/font-awesome/4.2.0/css/font-awesome.min.css"> 
                    <script src="http://cdn.bootcss.com/jquery/2.1.3/jquery.min.js"></script>
                </head>
                <style>
                   
                    table { 
                    table-layout: fixed;
                    word-wrap:break-word;
                    }
                </style>
                <body>
                    <table class="table table-hover" style="width:70%;hegiht:70%;">
                        <thead>
                            <tr>
                              <th>http状态</th>
                              <th>url</th>
                            </tr>
                        </thead>
                        <tbody>
    '''
    with open(filename, 'a') as wf:
        wf.write(head)

def saveFoot(filename):
    head = '''
                        </tbody>
            </table>
        </body>
    </html>
    '''
    with open(filename, 'a') as wf:
        wf.write(head)

def saveResult(filename, result):
    html = "<tr>"
    html += '<td>' + result['status_code'] + '</td>'
    html += '<td><a href="' + result['url'] + '" target="_blank">' + result['url'] + '</a></td>'
    html += '</tr>'
    with open(filename, 'a') as wf:
        wf.write(html)


if __name__ == '__main__':
    filename = os.path.split(os.path.realpath(__file__))[0] + '\\result\\' + datetime.now().date().strftime('%Y%m%d') + "_"+ str(random.randint(1, 88888)) + ".html"
    word_queue = build_wordlist(wordlist_file)
    #extensions = [".php", ".bak", ".inc"]  # ".php~", ".asp", ".aspx", ".jsp", ".jspx", ".mdb", ".orgi"
    extensions = ""
    saveHead(filename)
    for i in range(m):
        t = threading.Thread(target=dir_bruter, args=(word_queue, extensions,))
        threads.append(t)
        t.start()

    for q in threads:
        words.put('quit')

    for t in threads:
        t.join()
    saveFoot(filename)
    print '[+] all directory scanned Done.'