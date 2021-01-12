# browser_auto_foods.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome = webdriver.Chrome("./driver/chromedriver.exe")
chrome.get("https://www.yodobashi.com/")

# 検索ワード入力
search_box = chrome.find_element_by_name("word")
search_words = "jn810"

# 検索実行
search_box.send_keys(search_words)
search_box.send_keys(Keys.RETURN)
search_box = chrome.find_element_by_name("word")

text=chrome.find_element_by_class_name("pImg")
text.click()
chrome.switch_to.window(chrome.window_handles[1])
