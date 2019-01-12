import requests
import urllib.parse 
from bs4 import BeautifulSoup
import time

start = time.time()
INDEX = 'https://ck101.com/forum-3419-1.html'
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}
#headers: 將要求包裝成瀏覽器之後送出的方法，在此為包裝成Chrome
keyWord = ''
limitt, limittt = 0,0

def ListTheRow (url):
	page = requests.get(url,headers = headers)
	respond = BeautifulSoup(page.text, 'html.parser')
	soup = respond.find_all('tbody','threadrow')
	LikeMost = []
	for name in soup :
		Title = name.find('a','s xst').get('title')
		Like = name.find('span','thankNum').getText()
		see = name.find('span','viewNum').getText()
		Like = Like.replace('K','00').replace('.','').replace(' ','')
		see = see.replace('K','00').replace('.','').replace(' ','')
		try :
			global keyWord 
			if ( keyWord in Title and int (Like) >= limitt and int(see) >= limittt):
				member= {'Likes':Like, 'Name': Title, 'view': see}
				LikeMost.append(member)
		except :
			continue
	
	nextPage = respond.find('a','nxt').get('href')
	
	return LikeMost, nextPage

def NewPage(PageNumber):
	pageUrl = INDEX
	allPosts = []
	for i in range(PageNumber):
		posts, link = ListTheRow (pageUrl)
		allPosts = posts
		pageUrl = urllib.parse.urljoin(INDEX, link)
	return allPosts

if __name__ == '__main__':
	pages = int(input('想搜尋的頁數為：'))
	keyWord = input('關鍵字為：')
	limitt = int(input('感謝數：'))
	limittt = int(input('觀看數：'))
	for Page in range(1,pages+1):
		print ('第',Page,'頁：')
		for post in NewPage(Page):
			print (post['Likes'], post['Name'], post['view'])
	end = time.time()
	elapsed = end - start
	print ("Time taken: ", round(elapsed,3), "seconds.")
