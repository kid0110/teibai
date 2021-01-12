import keepa
import pandas as pd
import matplotlib
import requests
import datetime
import time
import schedule

#LINEに通知する
def send_line_notify(notification_message):
    line_notify_token = 'z57RXvbMukJTifFtROIVuLkuScy2skFxVG60a1xrjh3'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': "Bearer " + line_notify_token}
    data = {'message': notification_message}
    requests.post(line_notify_api, headers = headers, data = data)

#楽天のAPIを呼び出す
def Rakuten_api(jan_code):
    url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706'

    params = {
        'applicationId': '1083938945783823235',
        'keyword': jan_code,
        'sort': '+itemPrice'
    }

    r = requests.get(url,params=params)
    resp = r.json()

    #最低価格とショップ名を返す
    return resp['Items'][0]['Item']['itemPrice'],resp['Items'][0]['Item']['shopName']

#ヤフショのAPIを呼び出す
def Yahoo_api(jan_code):
    url = 'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch'

    params = {
        'appid': 'dj00aiZpPUNuaW5OSjZtclp5MiZzPWNvbnN1bWVyc2VjcmV0Jng9ZDk-', 
        'jan_code': jan_code,
        'sort': '+price'
    }

    r = requests.get(url,params=params)
    resp = r.json()

    #最低価格とショップ名を返す
    return resp['hits'][0]['price'],resp['hits'][0]['seller']['name']

#KeepaのAPIを呼び出す
def Keepa_api(jan_code):
    accesskey= '1kjpjviqg2q30r3u32o4lnc96bacjj62p2hcpoj1qgnk70j7gqqe1poffs6cnncr'

    api=keepa.Keepa(accesskey)

    return api.query(jan_code,domain='JP',buybox=True,product_code_is_asin=False)

#メイン処理
def job():

    jancodes = []

    f = open('jan_list.txt','r')

    jan_codes = f.read().splitlines()

    for jan_code in jan_codes:

        #KEEPA
        Keepa_product = Keepa_api(jan_code)
        #Amazon商品タイトル
        Amazon_title = Keepa_product[0]['title']
        #Amazon最新新品価格
        Amazon_NEW_price = Keepa_product[0]['data']['NEW'][-1]
        Amazon_Buybox_price = Keepa_product[0]['data']['BUY_BOX_SHIPPING'][-1]

        #楽天
        Rakuten_product,Rakuten_shop = Rakuten_api(jan_code)

        #ヤフショ
        Yahoo_product,Yahoo_shop = Yahoo_api(jan_code)

        #Lineに通知
        message="\n{0}\nAmazon_NEW_price:{1} Amazon_BUYBOX_price:{2}\nRakuten_price:{3} Rakuten_shop:{4}\nYahoo_price:{5} Yahoo_shop:{6}"\
        .format(Amazon_title,Amazon_NEW_price,Amazon_Buybox_price,Rakuten_product,Rakuten_shop,Yahoo_product,Yahoo_shop)
        send_line_notify(message)


#スケジュール処理
schedule.every(60).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)