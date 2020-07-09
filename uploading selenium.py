from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, requests, json, sys, os, shutil
from bs4 import BeautifulSoup
import pandas as pd

def login (website, account, password):
	driver.maximize_window()
	driver.get(website)
	elem = driver.find_element_by_id('uid')
	elem.clear()
	elem.send_keys(account)
	driver.implicitly_wait(1)
	passw = driver.find_element_by_id('password')
	passw.clear()
	passw.send_keys(password)
	driver.implicitly_wait(1)
	driver.find_element_by_name('Submit').click()
	time.sleep(7)

class siteObject (object):
	def __init__(self, site):
		self.site = site
		self.name = site.split('\\')[-1]
		self.inputDocu(site)
	def inputDocu(self, site):
		docList = os.listdir(site)
		self.docu = [*map(lambda x: site+'\\'+x, docList)]
	def remove(self):
		shutil.rmtree( self.site, ignore_errors=True)

def upload(app):
	#driver.get('http://app-eu.huawei.com/sdcp/portalNew#!isd/webix/rolloutPlanManagment.html')
	try:
		element = WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[title="Searches Customer Site ID and Customer Site Name and DU ID and DU Name"]')))
	except:
		print ('%s appears error!'%app.name)
	driver.find_element_by_css_selector('[title="Searches Customer Site ID and Customer Site Name and DU ID and DU Name"]').clear()
	driver.find_element_by_css_selector('[title="Searches Customer Site ID and Customer Site Name and DU ID and DU Name"]').send_keys(app.name)
	driver.find_element_by_css_selector('[id="aGlobalSearch"]').click()
	try:
		element = WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="webix_ss_body"]')))
	except:
		print ('%s appears error!'%app.name)
	#driver.find_element_by_xpath('//*[@id="rptable1554217078716"]/div[2]/div[1]/div/div[1]/div/input').click()
	time.sleep(1)
	driver.find_element_by_css_selector('[class="webix_ss_body"]').find_element_by_css_selector('[class="webix_ss_center_scroll"]').find_element_by_css_selector('[class="webix_column  webix_first"]').find_element_by_css_selector('[class="webix_table_checkbox"]').click()
	driver.find_element_by_css_selector('[id="batchUploadDrop_13089001"]').click()
	try:
		driver.find_element_by_xpath('//*[@id="batchUploadUl_13089001"]/li[2]').click()
	except:
		driver.find_element_by_css_selector('[id="batchUploadDrop_13089001"]').click()
		driver.find_element_by_xpath('//*[@id="batchUploadUl_13089001"]/li[2]').click()
	# Next page
	time.sleep(1)
	totalpage = driver.window_handles
	driver.switch_to_window(totalpage[-1])
	try:
		element = WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//*[@id="taskFileManageFileTypeGrdTable"]/tbody[2]/tr[6]/td[2]/a')))
	except:
		print ('%s appears error!'%app.name)
	listOfEle = driver.find_elements_by_xpath('//*[@id="taskFileManageFileTypeGrdTable"]/tbody[2]/tr')
	for i in listOfEle:
		if i.find_element_by_css_selector('[_col="2"]').text == 'Y':
			i.find_element_by_css_selector('[_col="1"]').find_element_by_css_selector('[title="Upload"]').click()
			break
	time.sleep(1)
	totalpage = driver.window_handles
	driver.switch_to_window(totalpage[-1])
	try:
		element = WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[type="file"]')))
	except:
		print ('%s appears error!'%app.name)
	for i in app.docu:
		driver.find_element_by_css_selector('[type="file"]').send_keys(i)
		break
	time.sleep(1)
	while True:
		totalpage = driver.window_handles
		if len(totalpage) == 2:
			driver.switch_to_window(totalpage[-1])
			break
		else:
			time.sleep(3)
	try:
		element = WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//*[@id="taskFileManageUnstructGrdTable"]/tbody[2]/tr/td[1]')))
	except:
		print ('%s appears error!'%app.name)
	driver.find_element_by_xpath('//*[@id="callBackButton"]').click()
	try:
		element = WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jalor_dialog1"]/div[3]/span')))
	except:
		print ('%s appears error!'%app.name)
	driver.find_element_by_xpath('//*[@id="jalor_dialog1"]/div[3]/span').click()
	driver.find_element_by_xpath('//*[@id="callBackButton"]').click()
	time.sleep(1)
	totalpage = driver.window_handles
	driver.switch_to_window(totalpage[0])
	print ('%s Done!'% app.name)
	app.remove()


def main (website, account, password, PathForListOfSite):
	login(website, account, password)
	listOfSite = os.listdir(PathForListOfSite)
	listOfSite = [*map(lambda x: PathForListOfSite+'\\%s'%x, listOfSite)]
	timer = 0
	for i in listOfSite:
		eachSite = siteObject(i)
		if len(eachSite.docu) != 0:
			upload(eachSite)
		else:
			print(eachSite.name)

if __name__ == '__main__':
	account = 'My account'
	password = 'My password'
	website = 'internal website'
	PathForListOfSite = r'C:\Users\jwx611578\Desktop\document'
	option = webdriver.ChromeOptions()
	option.add_argument('--window-size=1920,1080')
	option.add_argument('--start-maximized')
	option.add_argument("--log-level=3")
	driver = webdriver.Chrome( options=option)
	main(website, account, password, PathForListOfSite)