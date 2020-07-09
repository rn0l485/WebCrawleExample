from Cell import cell
import numpy as np  

class CellNet(object):
	def __init__ (self):
		self.centeral = cell( site = [0,0])
		self.NetList = np.empty((100, 100),dtype=cell)
		self.NetList[0][0] = self.centeral

	def reshape(self, shape):
		i,j = shape
		if i > 100 or j > 100: 
			if i<100:
				i = 100
			if j<100:
				j = 100
			NewList = np.empty((i+1, j+1),dtype=cell)
			for xEle in range(len(self.NetList)):
				for yEle in range(len(self.NetList[xEle])):
					NewList[xEle][yEle] = self.NetList[xEle][yEle]
			self.NetList = NewList

	def AddCell(self, site, infos):
		self.reshape(site)
		i,j = site
		self.NetList[i][j] = cell(site, N= self.CellExist([i,j+1]), E= self.CellExist([i+1,j]), W= self.CellExist([i-1,j]), S= self.CellExist([i,j-1]), info= infos)
		
	def CellExist(self, site):
		i,j = site 
		try :
			return self.NetList[i][j] 
		except :
			return None 
	
	def CheckCell (self, site):
		if self.CellExist(site) != None:
			cellInfo = {
				'cellN': self.CellExist(site).N,
				'cellE': self.CellExist(site).E,
				'cellW': self.CellExist(site).W,
				'cellS': self.CellExist(site).S,
				'infomation': self.CellExist(site).info
			}
			return cellInfo
		else :
			return None 

'''
if __name__ == '__main__':
	#test
	shapeX = int(input('the shape: '))
	shapeY = int(input('the shape: '))
	test1 = CellNet()
	test1.AddCell([shapeX,shapeY])
	print (test1.CheckCell([shapeX,shapeY]))
'''