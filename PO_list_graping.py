from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, datetime, requests, json, re
import pandas as pd 
from bs4 import BeautifulSoup
from distributed import Client
from distributed import as_completed


def ReadRequest (request, indexSheet, colname):
	requestment = list(request)
	requestSheet = indexSheet[indexSheet[colname].isin(requestment)]
	return requestSheet
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
def error_info_page(x):
	try:
		error_image = x.find('span')
		return True
	except:
		return False
def add_url(x):	
	x[12] = "http://isales.huawei.com/isales/mce/po/services/isalesmce/po/perf/profile/findPurchaseOrderByPermission?contractId=%s&startThread=1&findPilotArea=1"%(x[12])
	if x[5] != None:
		x[5] = x[5].split('T')[0]
	if x[14] != None:
		try:
			x[14] = re.search(r'[0-9]+\_[0-9]+',x[14]).group(0)
		except:
			x[14] = None 
	if x[15] != None:
		try:
			x[15] = re.search(r'[0-9]+\_[0-9]+',x[15]).group(0)
		except:
			x[15] = None 
	return x
def judging(total_PO):
	for k in range(len(total_PO[12])):
		if ('po.automation.check.deliveryProjectNo' in total_PO[12][k])|('automation.check.businessModeIntegration' in total_PO[12][k])|('automation.check.deliverySubProjectNo' in total_PO[12][k])|('automation.check.issuedDate' in total_PO[12][k])|('po.automation.check.quantity' in total_PO[12][k])|('No PO lines' in total_PO[12][k])|('t find Site ID in PO line' in total_PO[12][k])|('PO Line information is missing' in total_PO[12][k])|('t find the Header Reserve1 from PO line' in total_PO[12][k])|('t find suitable contract naming rule for this PO' in total_PO[12][k])|('Please Select Tax Id' in total_PO[12][k])|('the po line data is blank' in total_PO[12][k])|('Tax Application Country Check Failed' in total_PO[12][k])|('Tax Application Country are missing' in total_PO[12][k])|('without node id' in total_PO[12][k]):
			if ('po.automation.check.quantity' in total_PO[12][k])|('No PO lines' in total_PO[12][k])|('PO Line information is missing' in total_PO[12][k])|('t find the Header Reserve1 from PO line' in total_PO[12][k])|('t find suitable contract naming rule for this PO' in total_PO[12][k])|('the po line data is blank' in total_PO[12][k]):
				total_PO[12][k] = '1.2'
			elif ('Please Select Tax Id' in total_PO[12][k])|('Tax Application Country Check Failed' in total_PO[12][k])|('Tax Application Country are missing' in total_PO[12][k]):
				total_PO[12][k] = '1.3'
			elif ('automation.check.businessModeIntegration' in total_PO[12][k]):
				total_PO[12][k] = '1.1'	# basic info missing
			elif ('automation.check.issuedDate' in total_PO[12][k]):
				total_PO[12][k] = '1.4'
			elif ('No contract number or frame contract number' in total_PO[12][k]):
				total_PO[12][k] = '1.5'
			elif ('po.automation.check.deliveryProjectNo' in total_PO[12][k])|('automation.check.deliverySubProjectNo' in total_PO[12][k]):
				total_PO[12][k] = '1.6'
			else:
				total_PO[12][k] = '6'
		elif ('this PO line cannot associate PRE-PO line' in total_PO[12][k])|('this PO head associate multi PRE-PO head' in total_PO[12][k])|('po.auto.compare.errmsg.multiPREPOAssociate' in total_PO[12][k])|('po.message.checkAssociationBeforeSignOff' in total_PO[12][k])|('This PO not associate PRE-PO, does not need cancel' in total_PO[12][k])|('some PO lines can not find matching PRE-PO line' in total_PO[12][k])|(' this PO head associate no PRE-PO head' in  total_PO[12][k])|('Head associate failed' in total_PO[12][k])|('PO did not associate and compare with a Pre-PO' in total_PO[12][k])|('关联比对异常' in total_PO[12][k])|('noPREPOAssociate' in total_PO[12][k]):
			total_PO[12][k] = '2.0'		# need to judge the different type in type 2
		elif ('Item Unit Price Check Failed' in total_PO[12][k])|(("The following items" in total_PO[12][k])&('exist in Item Lib' in total_PO[12][k]))|('The following items are missing' in total_PO[12][k]):
			if ('Item Unit Price Check Failed' in total_PO[12][k]):
				if total_PO[4] == 'Equipment':
					total_PO[12][k] = '3.1'
				elif (total_PO[4] == 'Service')|(total_PO[4] == 'Integration'): 
					total_PO[12][k] = '3.3'
				else:
					total_PO[12][k] = '6'
			elif (("The following items" in total_PO[12][k])&(' exist in Item Lib' in total_PO[12][k]))|('The following items are missing' in total_PO[12][k]):
				if total_PO[4] == 'Equipment':
					total_PO[12][k] = '3.2'
				elif (total_PO[4] == 'Service')|(total_PO[4] == 'Integration'): 
					total_PO[12][k] = '3.4'
				else:
					total_PO[12][k] = '6'
			else:
				total_PO[12][k] = '3.0'
		elif ('A service BOQ submitted through the Configurator is required for a service contract or PO' in total_PO[12][k])|('The related PU is mandatory for BOQ' in total_PO[12][k])| ('Clear Sales Configuration Flag is required for an equipment BOQ' in total_PO[12][k])|('auto.boq.generating' in total_PO[12][k])|('CPart in the UPL does not exist' in total_PO[12][k])|('automation.rule.boq' in total_PO[12][k])|('checkpuNoboqNo' in total_PO[12][k])|('The BOQ is not in Accordance with the PU' in total_PO[12][k]):
			if total_PO[4] == 'Equipment':
				total_PO[12][k] = '4.1'
			elif (total_PO[4] == 'Service')|(total_PO[4] == 'Integration'): 
				total_PO[12][k] = '4.2'
			else:
				total_PO[12][k] = '6'
		elif ('find Site ID in PO line' in total_PO[12][k])|('integrate ACTIVE BUILD SUPPLIER from POR' in total_PO[12][k])|('samePo' in total_PO[12][k])|('amountoverflowframe' in total_PO[12][k])|('合同号已经存在' in total_PO[12][k])|('The sum of the PO amount is larger than the frame contract amount' in total_PO[12][k])|(('BusinessException' in total_PO[12][k])&('ROBOT校验&补全异常' in total_PO[12][k])):
			total_PO[12][k] = '5'
		elif('No error info' in total_PO[12][k]):
			total_PO[12][k] = '0'
		else:
			if not ('PO status is Published, Terminated, Cancelled, Pre-Closed, Closed, Signed ,or In Registration with PO lines' in total_PO[12][k]):
				total_PO[12][k] = '6'
	total_PO[12] = list(set(total_PO[12]))	
	return total_PO
def check_POR_subsub(PO_list):
	issueList = pd.DataFrame(columns = PO_list.columns)
	for i in range(len(PO_list)):
		each = list(PO_list.iloc[i]['description'])
		if '2.0' in each:
			issueList = issueList.append(PO_list.iloc[i])
	return issueList
def rewrite(PO_list, issue_list_si_dic):
	PO_list_new_des = []
	for i in range(len(PO_list)):
		if "2.0" in PO_list['description'][i]:
			PO_list_new_des.append(PO_list['description'][i].replace('2.0', issue_list_si_dic[PO_list['PO'][i]]))
		else:
			PO_list_new_des.append(PO_list['description'][i])
	return PO_list_new_des
def check_POR(PO_list, CNC, s):
	def k(x):
		if '2.3' in x['sinaria']:
			return '2.3'
		elif '2.2' in x['sinaria']:
			return '2.2'
		elif '2.1' in x['sinaria']:
			return '2.1'
		else:
			return '2'
	header = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-TW,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en;q=0.6',
		'Connection': 'keep-alive',
		'Content-Length': '20',
		'Content-Type': 'application/json; charset=UTF-8',
		'HAEHead': "{'version':'1.0','format':'json','rtype':'sync','batch':'no','rtype-policy':'','region':'szx','pageId':'swbf9HkgeUcLcwzkXOxKm12:1550569475129'}",
		'Host': 'ebusiness-uk.huawei.com',
		'Origin': 'http://ebusiness-uk.huawei.com',
		'Referer': 'http://ebusiness-uk.huawei.com/vdf/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest',
	}
	POR_issue = check_POR_subsub(PO_list)
	if len(list(POR_issue['PO'])) != 0:
		issue_list = ReadRequest(POR_issue['PO'], CNC, 'PO No')
		POR_searching = list(set(list(issue_list['NR_ID'])))
		POR_issue_list = {
			'2.3ForChecking':[],
			'2.2ForChecking':[],
			'2.1ForChecking':[],
		}
		for i in range(len(POR_searching)):
			info = s.post('http://ebusiness-uk.huawei.com/vdf/services/hmallservice.ukVdf.por.findPor/list/1/500/default/%5B%5D', headers = header, data = json.dumps({'nr_id': str(POR_searching[i])}))
			info = json.loads(info.text)
			time.sleep(1)
			for k in info['BO']:
				data = {
					'category': "undefined",
					'nrId': k['nr_id'],
					'porNo': k['por_no'],
					'siteId': k['site_id'],
					'total_price': str(k['total_price']),
					'version': k['version'],
					'version_id': k['version_id'],
				}
				data = json.dumps(data)
				line_info = s.post('http://ebusiness-uk.huawei.com/vdf/services/hmallservice.ukVdf.por.findMaterial/list/1/100/default/%5B%5D', headers = header, data = data)
				line_info = json.loads(line_info.text)			# po lines must lower than 100
				time.sleep(1)
				lines = []
				for j in line_info['BO']:
					POR_issue_list['2.1ForChecking'].append(str(POR_searching[i])+str(j['material_id'])+str(j['po_quantity']))
					POR_issue_list['2.2ForChecking'].append(str(POR_searching[i])+str(j['material_id'])+str(j['price_m']))
					POR_issue_list['2.3ForChecking'].append(str(POR_searching[i])+str(j['material_id']))
			print ('done %d' %(i+1))
		POR_issue_list = pd.DataFrame(data=POR_issue_list)
		arr1 = [*map(lambda x, y: str(x)+str(y) if '_' in x else 'blank',list(issue_list['NR_ID']), list(issue_list['Item Code']))]
		issue_list.insert(0, '2.3ForChecking', arr1)
		arr2 = [*map(lambda x, y, z: str(x)+str(y)+str(z) if '_' in x else 'blank',list(issue_list['NR_ID']), list(issue_list['Item Code']), list(issue_list['Discounted Unit Price']))]
		issue_list.insert(0, '2.2ForChecking', arr2)
		arr3 = [*map(lambda x, y, z: str(x)+str(y)+str(z) if '_' in x else 'blank',list(issue_list['NR_ID']), list(issue_list['Item Code']), list(issue_list['Quantity']))]
		issue_list.insert(0, '2.1ForChecking', arr3)
		arr4 = checking_POR_sub(issue_list, POR_issue_list)
		issue_list.insert(0, 'sinaria', arr4)
		issue_list_si = issue_list.groupby(by = 'PO No')['sinaria'].max().reset_index()
		issue_list_si_dic = {}
		for k in range(len(issue_list_si)):
			issue_list_si_dic[str(issue_list_si['PO No'][k])] = str(issue_list_si['sinaria'][k])
		PO_list = change_to_string(PO_list)
		PO_list['description'] = rewrite(PO_list, issue_list_si_dic)
	else:
		PO_list = change_to_string(PO_list)		
	return PO_list
def checking_POR_sub(issue_list, POR_issue_list):
	result = []
	for i in range(len(issue_list)):
		if (not issue_list.iloc[i]['2.3ForChecking'] in POR_issue_list['2.3ForChecking'] ):
			result.append(2.3)
		elif (not issue_list.iloc[i]['2.2ForChecking'] in POR_issue_list['2.2ForChecking'] ):
			result.append(2.2)
		elif (not issue_list.iloc[i]['2.1ForChecking'] in POR_issue_list['2.1ForChecking'] ):
			result.append(2.1)
		else:
			result.append('2')
	return result
def change_to_string(PO_list):
	descriptionList = []
	for i in range(len(PO_list)):
		descriptionList.append(','.join(PO_list.iloc[i]['description']))
	PO_list['description'] = descriptionList
	return PO_list
def drop_duplicate(total_PO, total_PO_duplicate, invalid_status):
	for PO_du in total_PO_duplicate:
		tem = []
		tem_version = []
		popuplist = []
		for PO in range(len(total_PO)):
			if total_PO[PO][0] == PO_du:
				popuplist.append(PO)
		for i in popuplist:
			tem.append(total_PO.pop(i))
		for temple in tem:
			tem_version.append(float(temple[16]))
		maxi = 0.0
		for i in tem_version:
			if i>maxi:
				maxi = i
		try:
			maxi = tem_version.index(maxi)
			total_PO.append(tem[maxi])
		except:
			for i in tem:
				if i[3] in invalid_status:
					total_PO.append(i)
	return total_PO
def main(account, password, DateOfToday, client, CNC):
	login('http://isales.huawei.com/isales/mce/po/#!servlet/configedPageServlet/isalesmce/po/info/listPurchaseOrder.html?type=pdq&entity=6&hidemenu=1&hidefoot=1&hideheader=1', account, password)
	cookies = driver.get_cookies()
	s=requests.Session()
	c = requests.cookies.RequestsCookieJar()
	for item in cookies:
		c.set(item["name"],item["value"])
	s.cookies.update(c)
	page = s.get("http://isales.huawei.com/isales/mce/po/services/isalesmce/po/profile/findPurchaseOrderPageList/list/page/500/1/%5B%7B%22fn%22%3A%22bas_org_dimension_t.REGION_ORG_ID%22%2C%22ft%22%3A0%2C%22fr%22%3A%22string%22%2C%22fv%22%3A%221-1CU-93%22%7D%2C%7B%22fn%22%3A%22bas_org_dimension_t.REP_OFFICE_ORG_ID%22%2C%22ft%22%3A0%2C%22fr%22%3A%22string%22%2C%22fv%22%3A%221-1CU-112%22%7D%2C%7B%22fn%22%3A%22SALE_CONTRACT_T.ISSUE_DATE%22%2C%22ft%22%3A0%2C%22fr%22%3A%22date%22%2C%22fv%22%3A%222018-01-01T00%3A00%3A00.000%2B0800%2C"+"%s"%(DateOfToday)+"T00%3A00%3A00.000%2B0800%22%7D%2C%7B%22fn%22%3A%22SALE_CONTRACT_T.CLOUD_DATA_FLAG%22%2C%22ft%22%3A0%2C%22fr%22%3A%22string%22%2C%22fv%22%3A%22Y%22%7D%2C%7B%22fn%22%3A%22FINBAS_CUSTOMER_ACCOUNT_V.customer_group%22%2C%22ft%22%3A0%2C%22fr%22%3A%22string%22%2C%22fv%22%3A%22Vodafone%22%7D%5D?viewMode=8")
	page_text = json.loads(page.text)
	total_pages = int(page_text['pageVO']['totalPages'])
	total_PO = []
	total_PO_duplicate = []
	for k in range(1, total_pages+1):
	#for k in range(1, 2):
		for i in page_text['result']:
			if i['primarySignEntityName'] == "Huawei Technologies (UK) Co., Ltd.":
				PO = [
					i['custContractNo'],			#0
					i['hwContractNo'],
					i['primaryFrameContractName'],	#2
					i['contractStatus'],
					i['businessMode'],				#4
					i['issueDate'],
					str(i['prepoAssociationName']),		#6
					i['exportAmount'],
					i['exportCurrencyCode'],		#8
					i['exportAmountUsd'],
					i['sumEquipAmount'],			#10
					i['sumServiceAmount'],
					i['contractId'],				#12
					i['poLineExistFlag'],
					i['wholeSetId'],				#14
					i['comments'],
					i['version']					#16
				]
				total_PO.append(PO) 
				if not PO[0] in total_PO_duplicate:
					total_PO_duplicate.append(PO[0])
		try:
			page = s.get("http://isales.huawei.com/isales/mce/po/services/isalesmce/po/profile/findPurchaseOrderPageList/list/page/500/%d/"%(k+1)+"%5B%7B%22fn%22%3A%22bas_org_dimension_t.REGION_ORG_ID%22%2C%22ft%22%3A0%2C%22fr%22%3A%22string%22%2C%22fv%22%3A%221-1CU-93%22%7D%2C%7B%22fn%22%3A%22bas_org_dimension_t.REP_OFFICE_ORG_ID%22%2C%22ft%22%3A0%2C%22fr%22%3A%22string%22%2C%22fv%22%3A%221-1CU-112%22%7D%2C%7B%22fn%22%3A%22SALE_CONTRACT_T.ISSUE_DATE%22%2C%22ft%22%3A0%2C%22fr%22%3A%22date%22%2C%22fv%22%3A%222018-01-01T00%3A00%3A00.000%2B0800%2C"+"%s"%(DateOfToday)+"T00%3A00%3A00.000%2B0800%22%7D%2C%7B%22fn%22%3A%22SALE_CONTRACT_T.CLOUD_DATA_FLAG%22%2C%22ft%22%3A0%2C%22fr%22%3A%22string%22%2C%22fv%22%3A%22Y%22%7D%2C%7B%22fn%22%3A%22FINBAS_CUSTOMER_ACCOUNT_V.customer_group%22%2C%22ft%22%3A0%2C%22fr%22%3A%22string%22%2C%22fv%22%3A%22Vodafone%22%7D%5D?viewMode=8")
			time.sleep(1)
			page_text = json.loads(page.text)
			print ('Change page! page: %d'%(k+1))
		except:
			print('Stop!')
			break
	invalid_status = ['Published', 'Terminated', "Pre-Closed", "Closed", "Signed", "In Registration", "Cancelled"]
	total_PO = client.submit(drop_duplicate,total_PO, total_PO_duplicate, invalid_status)
	total_PO = total_PO.result()
	total_PO = client.map(add_url, total_PO)
	total_PO = as_completed(total_PO)
	total_PO = [*map(lambda x: x.result(), total_PO)]	
	for i in range(len(total_PO)):
		error_info = []
		if not total_PO[i][3] in invalid_status:
			time.sleep(1)
			page = s.get(total_PO[i][12])
			page = json.loads(page.text)
			print(total_PO[i][0])

			if ('exceptionMemo' in page):
				if (page['exceptionMemo'] != None):
					error_info.append(page['exceptionMemo'])

			if not ('hwContractNo' in page)|('primaryFrameContractName' in page):
				error_info.append('No contract number or frame contract number')

			if ('valResultList' in page):
				if (len(page['valResultList'])!=0):
					for k in page['valResultList']:
						error_info.append(k['checkResultDescI18nKey'])
			if error_info:
				total_PO[i][12] = error_info
			else:
				total_PO[i][12] = ['No error info']

		elif total_PO[i][13] == 'N':
			if type(total_PO[i][12]) == list :
				total_PO[i][12].append('No PO lines')
			else:
				total_PO[i][12] = ['No PO lines']
		else:
			total_PO[i][12] = ['PO status is Published, Terminated, Cancelled, Pre-Closed, Closed, Signed ,or In Registration with PO lines']
	total_PO = client.map(judging, total_PO)
	total_PO = as_completed(total_PO)	
	total_PO = [*map(lambda x: x.result(), total_PO)]

	total_PO_dict = {
		'PO':[], 
		'description':[], 
		'PO_type':[], 
		'status':[], 
		'HW_contract':[], 
		'HW_Frame':[], 
		'PO_Amount(USD)':[], 
		'PO_issued_date':[], 
		'POR':[], 
		'NR_ID':[],
	}

	for i in total_PO:
		total_PO_dict['PO'].append(i[0])
		total_PO_dict['description'].append(i[12])
		total_PO_dict['PO_type'].append(i[4])
		total_PO_dict['status'].append(i[3])
		total_PO_dict['HW_contract'].append(i[1])
		total_PO_dict['HW_Frame'].append(i[2])
		total_PO_dict['PO_Amount(USD)'].append(i[9])
		total_PO_dict['PO_issued_date'].append(i[5])
		total_PO_dict['POR'].append(i[6])
		if i[14]!= None:
			total_PO_dict['NR_ID'].append(i[14])
		elif i[15] != None:
			total_PO_dict['NR_ID'].append(i[15])
		else :
			total_PO_dict['NR_ID'].append(i[14])

	PO_list = pd.DataFrame(data=total_PO_dict)
	PO_list = check_POR(PO_list, CNC, s)
	writer = pd.ExcelWriter(r'C:\Users\jwx611578\Desktop\PO Register Dashboard\PO_list.xlsx')
	PO_list.to_excel(writer,'description', index = False)
	writer.save()
	driver.quit()
if __name__ =='__main__':
	account = 'My account'
	password = 'My password'
	CNCpath = r'C:\Users\jwx611578\Desktop\CNC Sheet\last\CNC 2019-02-27.xlsx'

	client = Client('127.0.0.1:8786',processes=False)
	today = datetime.date.today()
	today = str(today)

	CNC = pd.read_excel(CNCpath)

	option = webdriver.ChromeOptions()
	option.add_argument('--window-size=1920,1080')
	option.add_argument('--start-maximized')
	option.add_argument("--log-level=3")
	option.add_argument('--headless')
	driver = webdriver.Chrome( executable_path=r'C:\Users\jwx611578\Desktop\useless\chromedriver', options=option)
	main(account, password, today, client, CNC)

