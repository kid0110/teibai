import keepa
import pandas as pd
import matplotlib
import requests
import datetime
import time
import schedule
import csv
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import logging
import re

#sofmap ブラウザ操作
def Sofmap(keyword):

    chrome = webdriver.Chrome("./driver/chromedriver.exe")
    chrome.get("https://www.sofmap.com/")

    search_box = chrome.find_element_by_id("searchText")
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    time.sleep(20)
    try:
        chrome.find_element_by_xpath("//*[@id='change_style_list']/li[1]/a[2]").click()
    except:
        chrome.quit()
        return "nan","nan"

    try:
        price = chrome.find_element_by_class_name("price").text.replace('¥','').replace(',','')
        price = re.match('.*?(\d+).*', price)
        price = price.group(1)        
    except:
        price = "nan"

    #Xpathでカートに入れるボタンがあれば在庫あり判定
    try:
        chrome.find_element_by_xpath("//*[@id='purchase_area']/a[1]/input[2]")
        stock = "在庫あり"
    except:
        stock = "nan"        

    chrome.quit()

    return price,stock
    

print(Sofmap("switch"))