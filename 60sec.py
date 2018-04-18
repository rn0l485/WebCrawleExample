import requests 
import time
from bs4 import BeautifulSoup

url = input ('please input the url:\n')
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}

page = requests.get(url,headers = headers)
respond = BeautifulSoup(page.text, 'html.parser')
soup  = respond.find('div','transcript__inner')
sentences = soup.getText()

localtime = time.asctime( time.localtime(time.time()) )
time = localtime+'.txt'
with open(time, 'w', encoding = 'UTF-8') as f:
	for sentance in sentences:
		f.write(sentance)

