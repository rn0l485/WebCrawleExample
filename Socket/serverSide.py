# -*- coding: utf-8 -*-
import socket, json, time
import requests
from bs4 import BeautifulSoup
#from selenium import webdriver
class server(object):
     def __init__(self):
          self.get_connect()
          self.get_accept()
     def get_connect(self):
          self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.s.bind(('0.0.0.0', 1234))    #0.0.0.0開放全部連線位址，1234一樣是port
          self.s.listen(1)   #設定一次可以連線的數目，例如：5
          
     def get_accept(self):
          self.conn, addr = self.s.accept()   #accept抓連線來源
          print('現在連接位址：', addr)
          
     def get_recieve(self):
          data = self.conn.recv(1024)   #buffer
          data = data.decode('utf-8') 
          return data
     
     def close(self):
          self.s.close()
          self.conn.close()   #關掉server端和結束client的連線

     def send(self, data):
          data = data.encode('utf-8')
          self.conn.send(data)

def trying_first (session, header, account):
     #page = session.get('https://www.instagram.com/%s/'%account, headers = header)
     page = requests.get('https://www.instagram.com/%s/'%account, headers = header)
     page = BeautifulSoup(page.text, 'html.parser')
     info = page.find("script", attrs={"type": "application/ld+json"}).text
     info = json.loads(info)
     account = info['alternateName']
     name = info['name']
     if 'email' in info:
          email = info['email']
     else:
          email = 'blank'
     address = 'blank'
     if "address" in info:
          if "addressLocality" in info:
               address = info['address']['addressLocality']
               if "addressCountry" in info['address']:
                    address = address + ', ' + info['address']['addressCountry']
     if 'telephone' in info:
          phone = info['telephone']
     else:
          phone = 'blank'
     follower = page.find("meta", attrs={"property":"al:ios:app_store_id"}).get("content")
     total = [name, account, email, follower, address, phone]
     total = ','.join(total)
     return total

if __name__ == '__main__':
     session = None
     header = {
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
          'accept-encoding': 'gzip, deflate, br',
          'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',
          'cache-control': 'max-age=0',
          'cookie': 'ig_cb=1; rur=PRN; mid=XHHR8wAEAAEOu9YOsa7XjeW6IEYx; csrftoken=0lQW9Q2X1pdjqWpcFHJOl3VaPfwfmf5P; urlgen="{\"2a02:c7d:9be3:7300:6c87:4b16:a736:f732\": 5607}:1gxh7K:XU4KsRtnYKIXMWZAlxyIV9BVsWU"',
          'upgrade-insecure-requests': '1',
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
     }
     serverSide = server()
     print('Server On')
     while True:
          account = serverSide.get_recieve()
          try:
               data = trying_first (session, header, account)
               print('send!')

               serverSide.send(data)
          except:
               print('break!')
               serverSide.send('connection fail')
               serverSide.conn.close()
               serverSide.get_accept()












