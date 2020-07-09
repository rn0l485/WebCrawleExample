from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

account = input ('your account: ')
password = input ('your password: ')

driver = webdriver.Chrome('./chromedriver')
driver.get('https://pro.104.com.tw/hrm/psc/m4/f0400.action')

elem = driver.find_element_by_id('email')
elem.clear()
elem.send_keys(account)
password = driver.find_element_by_id('pwd')
password.clear()
password.send_keys(password)
elem.send_keys(Keys.RETURN)
time.sleep(10)
target = driver.find_element_by_id('punchCardBtn')
ActionChains(driver).move_to_element(target).click(target).perform()
driver.close()