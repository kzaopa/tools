#!/usr/bin/env python
#coding:utf-8
#Author:1975
#data:20170406
#v1.0

import sys,glob,os,re

global filesize
filesize = 73400320     #Defines the size of a file to read

'''
simple url script processing
'''
def _url(read_fn,write_fn,*args):
    w_fn = open(write_fn,'w+')
    for line in open(read_fn,'r').readlines(filesize):
        if line:
            w_fn.writelines("http://"+line.strip()+"\n")
            #w_fn.writelines("<a href=\""+line.strip()+"\">\n")
    w_fn.close()

#_url('subdomain_edu.cn.txt','subdomain.edu.cn.txt')


'''
content copy for txt and so..
'''
def _file(file_path,write_fn,*args):
    if not os.path.isdir(file_path):
        print 'folder nonexistent or path error'
        return
    file_list = os.listdir(file_path)		#Get file list
    w_fn = open(write_fn,'w+')
    for fn in file_list:
    	if fn[-3:] == '.cn':		#Determine the type of file to be read
    		read_fn = open(fn,'r')
    		w_fn.writelines(read_fn)
    w_fn.close()
    read_fn.close()

#_file('E:/666','subdomain.txt')

'''
from 90sec https://forum.90sec.org/forum.php?mod=viewthread&tid=8705
'''
def getDictList(dict):
    regx = '''[\w\~\`\!\@\#\$\%\^\&\*\(\)\_\-\+\=\[\]\{\}\:\;\,\.\/\<\>\?]+'''
    with open(dict) as f:
        data = f.read()
        return re.findall(regx, data)
 
def rmdp(dictList):
    return list(set(dictList))      #Duplicate removal
 
def fileSave(dictRmdp, out):
    with open(out, 'a') as f:
        for line in dictRmdp:
            f.write(line + '\n')
 
def _dic(read_fn,write_fn,*args):
    dictList = getDictList(read_fn)
    dictRmdp = rmdp(dictList)
    fileSave(dictRmdp, write_fn)

'''
exection~
'''
def operation():
    o_list = {"-a":_url,"-c":_file,"-d":_dic}
    try:
        o_list.get(sys.argv[1])(sys.argv[2],sys.argv[3])
        #operation(sys.argv[1],sys.argv[2],sys.argv[3])
    except:
        #pwd_file = os.path.basename(__file__)
        info = '''
        usage: file.py options file.txt file.txt
        example: file.py options input.txt output.txt
        -a   www.domain.com -->> http://www.domain.com
        -c   content copy for txt and so..
        -d   remove duplicate content
        '''
        print info
#print sys.argv
operation()
