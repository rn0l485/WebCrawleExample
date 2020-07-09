from Net import CellNet
from Cell import cell
import random


class Map (CellNet):
	def __init__(self, infos = None):
		super().__init__()
		self.centeral = cell( site = [0,0], info= infos)
		self.MetalList = ['gold', 'sliver', 'iron', 'copper']
		self.yourMetal = {
			'gold':0,
			'sliver':0,
			'iron':0,
			'copper':0
		}
	def createMap(self, hellMode = None):
		xLv = len(self.NetList)
		yLv = len(self.NetList[0])
		randomNumber = random.randint(0, xLv*yLv)
		if hellMode:
			randomNumber/=4
			randomNumber = int(randomNumber//1)
		for _ in range(randomNumber):
			RanX = random.randint(0, xLv)
			RanY = random.randint(0, yLv)
			if super().CellExist([RanX,RanY])==None:
				metal = self.MetalList[random.randint(0,3)]
				super().AddCell([RanX-1,RanY-1], infos= metal)

	def searchMetal(self):
		xLv = len(self.NetList)
		yLv = len(self.NetList[0])
		MetalMap = []
		for i in range(xLv):
			for j in range(yLv):
				if super().CheckCell([i,j])!= None and super().CheckCell([i,j])['infomation']!= None :
					MetalSite = {
						'X':i,
						'Y':j,
						'Metal':super().CheckCell([i,j])['infomation']
					}
					MetalMap.append(MetalSite)
		return MetalMap

	def mine(self, site, MetalMap):
		i,j = site
		t = 0
		for k in range(len(MetalMap)):
			if MetalMap[k]['X']==i and MetalMap[k]['Y']==j:
				M = self.MetalList.index(MetalMap[k]['Metal'])
				if M == 0:
					self.yourMetal['gold']+=1
				elif M == 1 :
					self.yourMetal['sliver']+=1
				elif M == 2 :
					self.yourMetal['iron']+=1
				elif M == 3 :
					self.yourMetal['copper']+=1
				t-=1
			t+=1
		if t == len(MetalMap):
			print ('Sorry! here has nothing! ')
		if self.yourMetal['gold']+self.yourMetal['sliver']+self.yourMetal['iron']+self.yourMetal['copper']==len(MetalMap):
			print ('Oh my God!!! You are so crazzy!!!')
		elif self.yourMetal['gold']+self.yourMetal['sliver']+self.yourMetal['iron']+self.yourMetal['copper']%10 == 0 and self.yourMetal['gold']+self.yourMetal['sliver']+self.yourMetal['iron']+self.yourMetal['copper']!=0:
			print ('Well done! You get',self.yourMetal['gold']+self.yourMetal['sliver']+self.yourMetal['iron']+self.yourMetal['copper'],'metals now!')

if __name__ == '__main__':
	test2 = Map('gold')
	question = input('Do you want to join the hell mode? (yes/no) ')
	if question == 'yes':
		test2.createMap(hellMode=True)
	else:
		test2.createMap()
	flag = True
	NewMap = test2.searchMetal()
	print ('The total metals are:',len(NewMap),'of 10000.')
	while (flag):
		say = input ('what do you want to say? ')
		if say == 'exit':
			flag = False 
		elif say == 'mining':
			flag2 = True
			keyin = 0
			while (flag2):
				Xp = input('X site: ')
				Yp = input('Y site: ')
				if Xp.isdigit() and Yp.isdigit():
					Xp = int(Xp)
					Yp = int(Yp)
					test2.mine([Xp,Yp], NewMap)
					print (test2.yourMetal)
					keyin+=1
				else :
					flag2 = False
					print ('You have try', keyin,'times this time!')
		else :
			print ('say something!')












		

