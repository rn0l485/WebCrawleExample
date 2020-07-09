import pandas as pd
import numpy as np
import xlwt

flag = True 
def func (functionSelect, data):
	if (functionSelect=='1'):
		for number in range (7):
			print (ReadSheet (data,number))
	elif (functionSelect=='2'):
		name = input ('請輸入指定客戶名稱：')
		for number in range (7):
			print (speci(ReadSheet (data,number), name))
		
	elif (functionSelect=='3'):
		for numbe in range (7):
			print (NoPay(ReadSheet( data, numbe)))
	elif (functionSelect=='exit'):
		global flag
		flag = False 
	else :
		print ('請重新輸入。')
def ReadSheet(excel,number):	
	sheetPage=excel.parse(number,skiprows=2)
	sheetPage.drop('Unnamed: 0', axis = 1,inplace=True)
	excel1 = sheetPage.dropna(subset=['金額(含稅)']).drop(42,axis=0)	
	return excel1

def NoPay (excel):
	select = excel.loc[excel['入帳日期'].isin(['NaT'])]
	return select

def speci(excel, name):
	select = excel.loc[excel['客戶名稱'].isin([name])]
	return select


if __name__ == '__main__':
	name = input ('程式名稱：')
	data = pd.ExcelFile(name)
	while (flag):
		functionSelect = input ('請輸入要做的事：1.查詢檔案全頁 2.查詢特定公司 3. 未繳帳公司明細 ：')
		func (functionSelect, data)

	
	




