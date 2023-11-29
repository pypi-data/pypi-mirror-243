import requests
import random
def read(tag):
	postdata = {'user':'share','secret':'everyone','action':'get','tag':tag}
	r = requests.post('http://tinywebdb.appinventor.space/api',data=postdata)
	lens = len(r.text)
	ans = r.text[17:lens-2]
	return ans 

def write(tag,value):
	postdata = {'user':'share','secret':'everyone','action':'update','tag':tag,'value':value}
	r = requests.post('http://tinywebdb.appinventor.space/api',data=postdata)
	return r.text

def auth():
	password = input("請輸入開發者認證碼")
	ans = read("BCSFECARLOS")
	if password == ans:
		print("密碼正確")
		write("BCSFECARLOS",random.randint(1,1000000))
		return True
	else:
		print("密碼錯誤,請詢問管理員")
		return False
