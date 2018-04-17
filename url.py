import requests 
import time
from bs4 import BeautifulSoup

url = input ('please type in the url.')
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}

page = requests.get(url,headers = headers)
respond = BeautifulSoup(page.text, 'html.parser')
soup = respond.find_all('div','row article-dual-body-item')
english, translate = [],[]
for text in soup:
	EC = text.find_all('div','col-lg-6')
	english.append(EC[0].getText())
	for trans in EC:
		translate.append(trans.getText())

localtime = time.asctime( time.localtime(time.time()) )
time = localtime+'.txt'
time2 = localtime+'_translate.txt'
f = open(time, 'w', encoding = 'UTF-8')
for sentance in english:
	f.write(sentance+'\n\n')
f.close()

f1 = open(time2, 'w', encoding = 'UTF-8')
for sentance in translate:
	f1.write(sentance+'\n\n')
f1.close()


