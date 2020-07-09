import selenium as se 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time, datetime, threading
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

def read_info():
	PO = driver.find_element_by_css_selector('[id="custPoNo"]').text.strip()
	try :
		HW_contract = driver.find_element_by_css_selector('[id="hwContractNo"]').value_of_css_property('title')
	except:
		HW_contract = 'Blank'
	try:
		HW_Frame = driver.find_element_by_css_selector('[id="primaryFrameContractName"]').value_of_css_property('title')
	except:
		HW_Frame = 'Blank'
	try:
		error_info = driver.find_element_by_css_selector('[class="errMsgSpan"]').text.strip()
	except :
		error_info = 'Blank'
	driver.close()
	windows = driver.window_handles
	driver.switch_to.window(windows[0])
	return [PO, error_info, HW_contract, HW_Frame]

def obtain_info(number, account, password):
	driver.find_element_by_xpath(('//table[@id="purchaseOrderGridTable"]/tbody[@class="igrid-data"]/tr[@_row="%d"]/td[4]'%number)).find_element_by_css_selector('[href="javascript:void(0);"]').click()
	time.sleep(3)
	windows = driver.window_handles
	driver.switch_to.window(windows[-1])
	try:
		return read_info()
	except:
		time.sleep(2)
		a = driver.switch_to.alert
		a.accept()
		time.sleep(5)
		driver.switch_to.window(windows[0])
		return ['invalid PO', 'Blank']

def obtain_loop(line, account, password):
	PO_status = []
	for i in range(line):
		PO = obtain_info(i, account, password)
		PO_status.append(PO)
		time.sleep(1)
	return PO_status

def each_page (account, password):
	lines = len(driver.find_element_by_css_selector('[id="purchaseOrderGridTable"]').find_elements_by_tag_name('tr'))-1
	PO_status = obtain_loop(lines, account, password)
	return PO_status

def select_requestment():
	driver.find_element_by_css_selector('[id="contractStatus"]').click()	# status
	driver.find_element_by_css_selector('[val="Draft"]').click()

	driver.find_element_by_css_selector('[i18nkey="isales.base.pdq.more"]').click() # show more bottom

	driver.find_element_by_css_selector('[displayfield="accountGroup"]').click() 	#account group
	driver.find_element_by_css_selector('[val="Vodafone"]').click()

	driver.find_element_by_css_selector('[name="cloudDataFlag"]').click()
	driver.find_element_by_css_selector('[id="cloudDataFlag_ddl"]').find_element_by_css_selector('[val="Y"]').click()

	driver.find_element_by_css_selector('[id="btnSearch"]').click()		# search
	time.sleep(3)

	driver.find_element_by_css_selector('[class="jalor-pager-pagesize"]').click()	# extend the sheet 
	driver.find_element_by_css_selector('[value="200"]').click()
	time.sleep(5)

def draft_PO(account, password):
	""" main app """
	login('The website url', account, password)
	select_requestment()

	pages = int(driver.find_element_by_css_selector('[class="jalor-pager-group numbtns"]').find_elements_by_tag_name('a')[-2].find_element_by_css_selector('[type="num"]').text.strip())
	total_PO_info = []
	for i in range(pages):

		current_page = driver.find_element_by_css_selector('[class="jalor-pager-page"]')		# trying to do the app here
		current_page.clear()
		current_page.send_keys(i+1)
		driver.find_element_by_css_selector('[type="goto"]').click()
		time.sleep(3)
		PO_status = each_page(account, password)
		total_PO_info.append(PO_status)
	write_to_excel(total_PO_info)

def write_to_excel(data):
	total_PO = {'PO':[], 'description':[], 'HW_contract':[], 'HW_Frame':[]}
	for i in data:
		for j in i:
			total_PO['PO'].append(j[0])
			total_PO['description'].append(j[1])
			total_PO['HW_contract'].append(j[2])
			total_PO['HW_Frame'].append(j[3])
	PO_list = pd.DataFrame(data=total_PO)
	writer = pd.ExcelWriter('PO_list.xlsx')
	PO_list.to_excel(writer,'description', index = False)
	writer.save()

def re_logig(account, password):
	driver.switch_to.frame(driver.find_element_by_css_selector('[class="jalor-dialog-iframe"]'))
	elem = driver.find_element_by_css_selector('[id="uid"]')
	elem.clear()
	elem.send_keys(account)
	driver.implicitly_wait(1)

	driver.find_element_by_css_selector('[id="password"]')
	passw.clear()
	passw.send_keys(password)
	driver.implicitly_wait(1)
	driver.find_element_by_css_selector('[value="Log In"]').click()
	time.sleep(5)

if __name__ == '__main__':
	account = 'my account'
	password = 'my Password'
	driver = webdriver.Chrome()
	draft_PO( account, password)
