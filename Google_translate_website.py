import requests 
import time
from bs4 import BeautifulSoup
from hanziconv import HanziConv

url = input ('please type in the url.')
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}

page = requests.get(url,headers = headers)
respond = BeautifulSoup(page.text, 'html.parser')
soup = respond.find_all('div','row article-dual-body-item')
english, TW = [],[]
for text in soup:
	EC = text.find_all('div','col-lg-6')
	english.append(EC[0].getText())
	TW.append(HanziConv.toTraditional(EC[1].getText()))

trans = []
for E in range(len(english)):
	trans.append(english[E])
	trans.append(TW[E])

localtime = time.asctime( time.localtime(time.time()) )
time = localtime+'.txt'
time2 = localtime+'_translate.txt'
with open(time, 'w', encoding = 'UTF-8') as f:
	for sentance in english:
		f.write(sentance+'\n\n')

with open(time2, 'w', encoding = 'UTF-8') as f1:
	for sentance in trans:
		f1.write(sentance+'\n\n')



