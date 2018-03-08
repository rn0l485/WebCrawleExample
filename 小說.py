import requests
import urllib.parse 
from bs4 import BeautifulSoup

INDEX = 'https://ck101.com/forum.php?mod=forumdisplay&fid=3419&orderby=views&typeid=2399&orderby=views&typeid=2399&filter=reply&page=1'
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}
#headers: 將要求包裝成瀏覽器之後送出的方法，在此為包裝成Chrome
def ListTheRow (url):
	page = requests.get(url,headers = headers)
	respond = BeautifulSoup(page.text, 'html.parser')
	soup = respond.find_all('tbody','threadrow')
	LikeMost = []
	for name in soup :
		Title = name.find('a','s xst').get('title')
		Like = name.find('span','thankNum').getText()
		try :
			if ('異界'in Title and int (Like) > 100 or 'K' in Like):
				member= {'Likes':Like, 'Name': Title,}
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
	pages = 10
	for Page in range(1,pages+1):
		print ('第',Page,'頁：')
		for post in NewPage(Page):
			print (post['Likes'], post['Name'])
