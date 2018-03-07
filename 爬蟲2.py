import requests
import urllib.parse 
from bs4 import BeautifulSoup

INDEX = 'https://worldofwarcraft.com/en-us/game/pvp/leaderboards/3v3'
allnum = 0
def playerList(url):
	pageResults = requests.get(url)
	soup = BeautifulSoup(pageResults.text, 'html.parser')
	character = soup.find_all('div','SortTable-row')
	player =[]
	for chara in character:
		try :
			playerLt = {
				'Name': chara.find('div','Character-name').getText().strip(),
				'Level': chara.find('div','Character-level').getText().strip(),
				'Rating': chara.find('div','SortTable-col SortTable-data text-nowrap align-center color-status-warning').getText().strip()
			}
			player.append(playerLt)
		except :
			global allnum
			allnum += 1
			continue
	next = soup.find('a','Link Button Button--ghost Button--small PageNumbers-button Button--next is-selected').get('href')
	return player, next

def nextPage(num):
    pageUrl = INDEX
    allPosts = []
    for i in range(num):
        posts, link = playerList(pageUrl)
        allPosts += posts

        pageUrl = urllib.parse.urljoin(INDEX, link)
    return allPosts

if __name__ == '__main__' :
	pages = 1
	for post in nextPage(pages):
		print (post['Name'], post['Level'], post['Rating'])
	print (allnum)


