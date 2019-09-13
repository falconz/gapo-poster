from argparse import ArgumentParser
import requests
import json
import time
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class GapoPoster:
	def __init__(self):
		self.loginURL = "https://api.gapo.vn/main/v1.0/auth/password-login"
		self.postURL = "https://api.gapo.vn/main/v1.0/post/create"
		self.profileURL = "https://gapo.vn/profile/"
		self.contentDantri = "https://dantri.com.vn/trangchu.rss"
		self.listPost = "https://api.gapo.vn/main/v1.0/post?expand=comments&from_id&limit=10&user_id="
		
		http_proxy  = "http://127.0.0.1:8081"
		https_proxy = "http://127.0.0.1:8081"
		ftp_proxy   = "http://127.0.0.1:8081"
		self.proxyDict = { 
					"http"  : http_proxy, 
					"https" : https_proxy, 
					"ftp"   : ftp_proxy
					}
	
	def checkPost(self,userInfo):
		url = self.listPost+str(userInfo['user']['id'])
		response = requests.get(url, headers={"Authorization":"Bearer "+userInfo['token']}, verify=False)
		if(response.status_code == 200):
			data = json_data = json.loads(response.text)
			return data
		else:
			return False
		
	
	def loginGapo(self,username,password):
		response = requests.post(self.loginURL, files={'phone': (None, username), 'password': (None, password)}, verify=False)
		if(response.status_code == 200):
			data = json_data = json.loads(response.text)
			return data
		else:
			return False
			
	def postThread(self,userInfo):
		content = self.genContent()
		response = requests.post(self.postURL, files={'content': (None, content), 'privacy': (None, 1), 'data_source': (None, 1)},headers={"Authorization":"Bearer "+userInfo['token']}, verify=False)
		if(response.status_code == 200):
			data = json_data = json.loads(response.text)
			return data
		else:
			return False
	
	def genContent(self):
		f = self.random_line('contents.txt')
		f = f+ self.random_line('contents.txt')
		f = f+ self.random_line('contents.txt')
		f = f+ "\r\n"+"#Ger"
		return f
		
	def random_line(self,afile):
		with open(afile,encoding='utf8') as f:
			lines = f.readlines()
			return random.choice(lines)
		
		

if __name__ == "__main__":
	message = 'Usage: python main.py -U <path_to_file>'
	h = '-U file argument'
	parser = ArgumentParser(description=message)
	parser.add_argument('-U', '--users', required=True, help=h)
	f = parser.parse_args()
	gapoClass = GapoPoster()
	while True:
		try:
			for user in open(f.users, 'r'):
				user = user.replace(" ", "")
				user = user.split("|")
				userInfo = gapoClass.loginGapo(user[0].rstrip(),user[1].rstrip())
				if(userInfo != False):
					post = gapoClass.checkPost(userInfo)
					if(len(post) > 0):
						postinDay = 0
						if(len(post)<3):
							rangepost = len(post)
						else:
							rangepost = 3
						for i in range(rangepost):
							current = time.time() 
							subtime = current - post[i]['create_time']
							if(subtime <= 86400):
								postinDay = postinDay +1
						if(postinDay < 3):
							print("Posting user:"+user[0].rstrip())
							gapoClass.postThread(userInfo)
					else:
						print("Posting user:"+user[0].rstrip())
						gapoClass.postThread(userInfo)
				else:
					print("Username or password invalid:" + user[0].rstrip() +"|"+user[1].rstrip())
			time.sleep(30)
		except Exception:
			pass