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
import re
import sys
import argparse

#LINEに通知する
def send_line_notify(notification_message):
    line_notify_token = 'z57RXvbMukJTifFtROIVuLkuScy2skFxVG60a1xrjh3'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': "Bearer " + line_notify_token}
    data = {'message': notification_message}
    requests.post(line_notify_api, headers = headers, data = data)

#現在の為替を取得する
def USD_JPY():
    url="https://stocks.finance.yahoo.co.jp/stocks/detail/?code=usdjpy"
    
    try:
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        d1 = soup.select_one(".stoksPrice").string
        return d1
    except:
        return 100

#楽天のAPIを呼び出す
def Rakuten_api(jan_code,Amazon_price):
    url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706'

    #Amazonの価格より30%より安い商品は切る
    min_price = int(Amazon_price * 0.3)

    params = {
        'applicationId': '1083938945783823235',
        'keyword': jan_code,
        'NGKeyword': "中古 レンタル 訳アリ 訳あり",
        'orFlag': 1,
        'availability': 1,
        'minPrice': min_price,
        'sort': '+itemPrice'
    }

    try:
        r = requests.get(url,params=params)
        resp = r.json()    
        return resp['Items'][0]['Item']['itemPrice'],resp['Items'][0]['Item']['shopName']
    except:
        return "nan","nan"

#ヤフショのAPIを呼び出す
def Yahoo_api(jan_code,Amazon_price):
    url = 'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch'

    #Amazonの価格より30%より安い商品は切る
    min_price = int(Amazon_price * 0.3)

    params = {
        'appid': 'dj00aiZpPUNuaW5OSjZtclp5MiZzPWNvbnN1bWVyc2VjcmV0Jng9ZDk-', 
        'jan_code': jan_code,
        'price_from': min_price,
        'sort': '+price',
        'condition': 'new',
    }

    try:
        r = requests.get(url,params=params)
        resp = r.json()
        return resp['hits'][0]['price'],resp['hits'][0]['seller']['name'],resp['hits'][0]['inStock']
    except:
        return "nan","nan","nan"


#ASINを引数にKeepaのAPIを呼び出す
def Keepa_api_ASIN(ASIN):
    accesskey= '1kjpjviqg2q30r3u32o4lnc96bacjj62p2hcpoj1qgnk70j7gqqe1poffs6cnncr'

    api = keepa.Keepa(accesskey)

    try:
        Keepa_product = api.query(ASIN,domain='JP',buybox=True,progress_bar=False)
    except:
        return "nan","nan","nan","nan","nan","nan","nan","nan"


    #Amazon商品タイトル
    try:
        Amazon_title = Keepa_product[0]['title']
    except:
        Amazon_title = "nan"

    #JANコード
    try:
        jan_code = Keepa_product[0]['eanList'][0]
    except:
        jan_code = "nan"

    #型番
    try:
        Amazon_partNumber = Keepa_product[0]['partNumber']
    except:
        Amazon_partNumber = "nan"

    #Amazon最新新品価格
    try:
        Amazon_NEW_price = Keepa_product[0]['data']['NEW'][-1]
        if(np.isnan(Amazon_NEW_price) == False):
            Amazon_NEW_price = float(Amazon_NEW_price)*100
    except:
        Amazon_NEW_price = "nan"
    
    #Amazon最新カート価格
    try:
        Amazon_Buybox_price = Keepa_product[0]['data']['BUY_BOX_SHIPPING'][-1]
        if(np.isnan(Amazon_Buybox_price) == False):
            Amazon_Buybox_price = float(Amazon_Buybox_price)*100
    except:
        Amazon_Buybox_price = "nan"

   #Amazon最新3回分価格の平均
    try:
        Amazon_Last1_price = Keepa_product[0]['data']['NEW'][-2]
        Amazon_Last2_price = Keepa_product[0]['data']['NEW'][-3]
        Amazon_Last3_price = Keepa_product[0]['data']['NEW'][-4]
        Amazon_Last3mean_price = (Amazon_Last1_price + Amazon_Last2_price + Amazon_Last3_price) / 3
        if(np.isnan(Amazon_Last3mean_price) == False):
            Amazon_Last3mean_price = float(Amazon_Last3mean_price)*100
    except:
        Amazon_Last3mean_price = "nan"

    #FBA手数料
    try:
        FBA_fee = Keepa_product[0]['fbaFees']['pickAndPackFee']
    except:
        FBA_fee = "nan"

    #ランキング
    try:
        Ranking = Keepa_product[0]['data']['SALES'][-1]
    except:
        Ranking = "nan"

    return Amazon_title,jan_code,Amazon_partNumber,Amazon_NEW_price,Amazon_Buybox_price,Amazon_Last3mean_price,FBA_fee,Ranking


#JANコードを引数にKeepaのAPIを呼び出す
def Keepa_api_JAN(jan_code):
    accesskey= '1kjpjviqg2q30r3u32o4lnc96bacjj62p2hcpoj1qgnk70j7gqqe1poffs6cnncr'

    api = keepa.Keepa(accesskey)

    try:
        Keepa_product = api.query(jan_code,domain='JP',buybox=True,product_code_is_asin=False,progress_bar=False)
    except:
        return "nan","nan","nan","nan","nan","nan","nan"


    #Amazon商品タイトル
    try:
        Amazon_title = Keepa_product[0]['title']
    except:
        Amazon_title = "nan"

    #型番
    try:
        Amazon_partNumber = Keepa_product[0]['partNumber']
    except:
        Amazon_partNumber = "nan"

    #Amazon最新新品価格
    try:
        Amazon_NEW_price = Keepa_product[0]['data']['NEW'][-1]
        if(np.isnan(Amazon_NEW_price) == False):
            Amazon_NEW_price = float(Amazon_NEW_price)*100
    except:
        Amazon_NEW_price = "nan"
    
    #Amazon最新カート価格
    try:
        Amazon_Buybox_price = Keepa_product[0]['data']['BUY_BOX_SHIPPING'][-1]
        if(np.isnan(Amazon_Buybox_price) == False):
            Amazon_Buybox_price = float(Amazon_Buybox_price)*100
    except:
        Amazon_Buybox_price = "nan"

   #Amazon最新3回分価格の平均
    try:
        Amazon_Last1_price = Keepa_product[0]['data']['NEW'][-2]
        Amazon_Last2_price = Keepa_product[0]['data']['NEW'][-3]
        Amazon_Last3_price = Keepa_product[0]['data']['NEW'][-4]
        Amazon_Last3mean_price = (Amazon_Last1_price + Amazon_Last2_price + Amazon_Last3_price) / 3
        if(np.isnan(Amazon_Last3mean_price) == False):
            Amazon_Last3mean_price = float(Amazon_Last3mean_price)*100
    except:
        Amazon_Last3mean_price = "nan"

    #FBA手数料
    try:
        FBA_fee = Keepa_product[0]['fbaFees']['pickAndPackFee']
    except:
        FBA_fee = "nan"

    #ランキング
    try:
        Ranking = Keepa_product[0]['data']['SALES'][-1]
    except:
        Ranking = "nan"

    return Amazon_title,Amazon_partNumber,Amazon_NEW_price,Amazon_Buybox_price,Amazon_Last3mean_price,FBA_fee,Ranking

#ヨドバシ ブラウザ操作
def Yodobashi(keyword):

    try:
        url = "https://www.yodobashi.com/?discontinued=true&word={0}".format(keyword)    
        chrome = webdriver.Chrome("./driver/chromedriver.exe")
        chrome.get(url)
        chrome.find_element_by_class_name("pImg").click()
        chrome.switch_to.window(chrome.window_handles[1])
    except:
        chrome.quit()
        return "nan","nan"

    try:
        price = chrome.find_element_by_class_name("productPrice").text
        price = price.replace('￥','').replace(',','')
    except:
        price = "nan"

    try:
        stock = chrome.find_element_by_id("salesInfoTxt").text
    except:
        stock = "nan"

    chrome.quit()

    return price,stock


#ビックカメラ ブラウザ操作
def Biccamera(keyword):

    #BOT対策でエラーになることがある
    try:
        chrome = webdriver.Chrome("./driver/chromedriver.exe")
        chrome.get("https://www.biccamera.com/bc/main/")
        search_box = chrome.find_element_by_name("q")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
    except:
        chrome.quit()
        return "nan","nan"

    try:
        chrome.find_element_by_class_name("cssopa").click()
    except:
        chrome.quit()
        return "nan","nan"

    try:
        price = chrome.find_element_by_class_name("bcs_price").text.replace(',','')
        price = re.match('.*?(\d+).*', price)
        price = price.group(1)
    except:
        price = "nan"

    try:
        stock = chrome.find_element_by_class_name("label_gray").text
    except:
        stock = "nan"

    chrome.quit()

    return price,stock


#ECカレント ブラウザ操作
def ECcurrent(keyword):

    #サイトサーバダウンの場合nanをreturn
    try:
        chrome = webdriver.Chrome("./driver/chromedriver.exe")
        chrome.get("https://www.ec-current.com/")
        search_box = chrome.find_element_by_name("keyword")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
    except:
        chrome.quit()
        return "nan","nan"         

    try:
        price = chrome.find_element_by_id("ctl00_lblPrice").text.replace('¥','').replace(',','')
    except:
        price = "nan"

    try:
        stock = chrome.find_element_by_id("ctl00_lblMsgStock").text
    except:
        stock = "nan"

    chrome.quit()

    return price,stock

#ヤマダ電機 ブラウザ操作
def Yamada(keyword):

    try:
        chrome = webdriver.Chrome("./driver/chromedriver.exe")
        chrome.get("https://www.yamada-denkiweb.com/")
        search_box = chrome.find_element_by_name("q")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
    except:
        return "nan","nan"

    #noitemというクラスがあれば終了
    #ヤマダモールで見つかる場合はexceptに入る
    try:
        chrome.find_element_by_class_name("noitem")
        chrome.quit()
        return "nan","nan"
    except:
        #ダミー処理
        a = 1

    try:
        price = chrome.find_element_by_class_name("item-price-box").text.replace('¥','').replace(',','')
        price = re.match('.*?(\d+).*', price)
        price = price.group(1)
    except:
        price = "nan"

    try:
        stock = chrome.find_element_by_class_name("note").text
    except:
        stock = "nan"

    chrome.quit()

    return price,stock

#ひかりTV ブラウザ操作
def HikariTV(keyword):

    #サイトサーバダウンの場合nanをreturn
    try:
        chrome = webdriver.Chrome("./driver/chromedriver.exe")
        chrome.get("https://shop.hikaritv.net/")    
        search_box = chrome.find_element_by_class_name("searchBox")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
    except:
        chrome.quit()
        return "nan","nan"        

    try:
        chrome.find_element_by_class_name("w50p_item_name").click()
        chrome.switch_to.window(chrome.window_handles[1])
    except:
        chrome.quit()
        return "nan","nan"

    try:
        price = chrome.find_element_by_class_name("num").text.replace(',','')
    except:
        price = "nan"

    try:
        stock = chrome.find_element_by_id("shippingStock").text
    except:
        stock = "nan"

    chrome.quit()

    return price,stock

#コジマ ブラウザ操作
def Kojima(keyword):

    #サイトサーバダウンの場合nanをreturn
    try:
        chrome = webdriver.Chrome("./driver/chromedriver.exe")
        chrome.get("https://www.kojima.net/ec/top/CSfTop.jsp")
        search_box = chrome.find_element_by_name("q")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
    except:
        chrome.quit()
        return "nan","nan"        

    try:
        chrome.find_element_by_class_name("tag_box").click()
    except:
        chrome.quit()
        return "nan","nan"

    try:
        price = chrome.find_element_by_class_name("price").text.replace(',','')
        price = re.match('.*?(\d+).*', price)
        price = price.group(1)
    except:
        price = "nan"

    try:
        point = chrome.find_element_by_class_name("point").text
    except:
        point = "nan"

    try:
        stock = chrome.find_element_by_class_name("deliverydate").text
    except:
        stock = "nan"

    chrome.quit()

    return price,stock

#Edion ブラウザ操作
def Edion(keyword):

    #サイトサーバダウンの場合nanをreturn
    try:
        chrome = webdriver.Chrome("./driver/chromedriver.exe")
        chrome.get("https://www.edion.com/")
        search_box = chrome.find_element_by_name("keyword")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
    except:
        chrome.quit()
        return "nan","nan" 

    try:
        chrome.find_element_by_class_name("item").click()
    except:
        chrome.quit()
        return "nan","nan"

    try:
        price = chrome.find_element_by_class_name("intaxPrice").text.replace('￥','').replace(',','')
        price = re.match('.*?(\d+).*', price)
        price = price.group(1)        
    except:
        price = "nan"

    #カートに入れるボタンがあるかどうかで判定
    try:
        chrome.find_element_by_id("into_cart").text
        stock = "在庫あり"
    except:
        stock = "在庫なし"

    chrome.quit()

    return price,stock

#Sofmap ブラウザ操作
def Sofmap(keyword):

    #サイトサーバダウンの場合nanをreturn
    try:
        chrome = webdriver.Chrome("./driver/chromedriver.exe")
        chrome.get("https://www.sofmap.com/")
        search_box = chrome.find_element_by_id("searchText")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
    except:
        chrome.quit()
        return "nan","nan"        

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

#オムニ7 ブラウザ操作
def Omni7(keyword):

    #サイトサーバダウンの場合nanをreturn
    try:
        chrome = webdriver.Chrome("./driver/chromedriver.exe")
        chrome.get("https://www.omni7.jp/top")
        search_box = chrome.find_element_by_id("keyword")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
    except:
        chrome.quit()
        return "nan","nan"          

    price = "nan"
    time.sleep(1)

    #txtLLがある場合、検索結果がないとみなし、returnする
    try:
        chrome.find_element_by_class_name("txtLL")
        chrome.quit()
        return "nan","nan"
    except:
        #ダミー操作
        a = 1

    try:
        chrome.find_element_by_class_name("productImg").click()
    except:
        chrome.quit()
        return "nan","nan"

    time.sleep(1)
    try:
        price = chrome.find_element_by_class_name("js-productInfoCampaignTax").text.replace(',','')
        price = re.match('.*?(\d+).*', price)
        price = price.group(1)        
    except:
        #ダミー処理
        a = 1

    try:
        price = chrome.find_element_by_class_name("js-productInfoPriceTax").text.replace(',','')
        price = re.match('.*?(\d+).*', price)
        price = price.group(1)        
    except:     
        #ダミー処理
        a = 1 

    try:
        stock = chrome.find_element_by_class_name("js-productInfoStockStatus").text
    except:
        stock = "nan"        

    chrome.quit()

    return price,stock


#価格差計算 手数料11%で計算
def diff_price(price1,price2,fee):
    try:
        return int(price1*0.89)-int(price2)-int(fee)
    except:
        return "nan"

#仕入判断
def Purchase_decision(selling_price,diff_price):
    try:
        #粗利率10%以上かつ粗利500円以上の場合1 それ以外の場合0
        if(diff_price/selling_price >= 0.1 and diff_price >= 500):
            return 1
        else:
            return 0
    except:
        return 0

#Keepa通知からASIN返す
def Keepa_Scraping():

    try:
        chrome = webdriver.Chrome("./driver/chromedriver.exe")
        chrome.get("https://keepa.com/#!notification")
        time.sleep(5)
        
        chrome.find_element_by_id("panelUserRegisterLogin").click()
        
        username = chrome.find_element_by_id("username")
        username.send_keys("k.hiroki0110@gmail.com")
        password = chrome.find_element_by_id("password")
        password.send_keys("kidooka1")
        time.sleep(2)
        password.send_keys(Keys.RETURN)
        time.sleep(2)
        ASIN = chrome.find_element_by_class_name("external").get_attribute("href")
        pattern = '.*asin=(\S{10})'
        ASIN = re.match(pattern, ASIN)
        return ASIN.group(1)
    except:
        return 0
        chrome.quit()

    chrome.quit()