#!/usr/bin/python
import time
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from time import sleep
#import socket
import sys

def dixie():
    t = time.time()
    browser = webdriver.Firefox()
    mainpage = 'http://www.richmond.com/news/local/city-of-richmond/poll-should-richmond-remove-its-confederate-monuments/poll_70452265-9c50-587f-886e-10bcb46dd990.html'

    browser.set_page_load_timeout(13)
    try: 
        browser.get(mainpage)
    except TimeoutException:
        browser.execute_script("window.stop();")

    #try:
        #wait = WebDriverWait(browser, 10, 0.25)
        ##wait.until(EC.element_to_be_clickable(By.XPATH('//input[@title="NO"]'))
        #wait.until(EC.element_to_be_clickable((By.ID, 'asset-content'))

        ##signal = WebDriverWait(browser,10).until(
        ##EC.presence_of_element_located((By.XPATH,'//input[@title="NO"]'))
        ##EC.presence_of_element_located((By.XPATH,'//input[@title="NO"]'))
    #)
    #finally:
        #browser.execute_script("window.stop();")
    sleep(1)
    nobut = browser.find_element_by_xpath('//input[@title="NO"]')
    nobut.click()
    subut = browser.find_element_by_class_name('btn-success')
    subut.click()
    sleep(5)

    #socket.setdefaulttimeout(6)
    #try:
        #browser.get(mainpage)
    #except socket.timeout:
        #nobut = browser.find_element_by_xpath('//input[@title="NO"]')
        #nobut.send_keys(Keys.ESCAPE)
        #nobut.click()
        #subut = browser.find_element_by_class_name('btn-success')
        #subut.click()
    #sleep(4)
    browser.quit()
dixie()
