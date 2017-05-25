from selenium import webdriver
from selenium.webdriver.common import keys
from time import sleep
from os import listdir,path
import re, csv
import sys

USER = '********'
PASS = '********'

browser = webdriver.Firefox()
mainpage = 'https://www.fedex.com/us'
createship = 'https://www.fedex.com/shipping/labelAction.do?method=doNewShip'

browser.get(mainpage)
#input > value > User ID
uid = browser.find_element_by_xpath('//input[@value="User ID"]')
uid.send_keys(USER)
#input > id > pswd-input
password = browser.find_element_by_id('pswd-input')
password.send_keys(PASS)
loginnow = browser.find_element_by_xpath('//*[@id="banner-login"]/form/button')
loginnow.click()

sleep(5)
namebutton = browser.find_element_by_id('toData.contactName._LookupButton')
namebutton.click()

namelist = browser.find_element_by_id('toData.contactName._InputSelect').find_elements_by_tag_name('option')

alreadyDone = [path.splitext(q)[0] for q in listdir('.') if q.find('.png') != -1]
optionvaluelist = [ q.get_attribute('value') for q in namelist if q.get_attribute('value')[0].isdigit() and q.get_attribute('value') not in alreadyDone ]

print('there are ' + str(len(optionvaluelist)) + ' records')
count = len(optionvaluelist)
## main loop
for optionvalue in optionvaluelist:
    browser.get(createship)
    namebutton = browser.find_element_by_id('toData.contactName._LookupButton')
    namebutton.click()
    nameentry = browser.find_element_by_xpath('//option[@value="' + optionvalue + '"]')
    nameentry.click()
    sleep(2.5)
    calbutton = browser.find_element_by_id('psd_shipDate._icon')
    calbutton.click()
    datewanted = browser.find_element_by_id('psd_shipDate._week5day6')
    datewanted.click()
    weightbox = browser.find_element_by_xpath('//input[@name="psdData.mpsRowDataList[0].weight"]')
    weightbox.send_keys("0.5")
    browser.find_element_by_id('completeShip.ship.field').click()
    sleep(2)
    imgurl = browser.find_element_by_id('labelImage').get_attribute('src')
    browser.get(imgurl)
    browser.find_element_by_tag_name('img').screenshot(optionvalue + '.png')
    count -= 1
    print(count,)
    sleep(0.5)
