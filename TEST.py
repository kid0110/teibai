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
from bs4 import BeautifulSoup
import library
import subprocess

def job():
    t1 = time.time()
    ASIN = library.Keepa_Scraping()

    Amazon_title,jan_code,Amazon_partNumber,Amazon_NEW_price,Amazon_Buybox_price,Amazon_Last3mean_price,FBA_fee,Ranking = library.Keepa_api_ASIN(ASIN)

    print("Amazon_NEW_price:{0}".format(Amazon_NEW_price))
    print("Amazon_Last3mean_price:{0}".format(Amazon_Last3mean_price))

    #過去3回の平均の8割より最新価格が安かったら
    #各サイトと比較を行う
    if(Amazon_Last3mean_price*0.8 > Amazon_NEW_price):
        print("価格下落アラート")
        print("楽天")
        Rakuten_price,Rakuten_shop = library.Rakuten_api(jan_code,Amazon_NEW_price)
        print("ヤフー")
        Yahoo_price,Yahoo_shop,Yahoo_inStock = library.Yahoo_api(jan_code,Amazon_NEW_price)
        print("ヨドバシ")
        Yodobashi_price,Yodobashi_stock = library.Yodobashi(Amazon_partNumber)
        print("ビック")
        Biccamera_price,Biccamera_stock = library.Biccamera(Amazon_partNumber)
        print("ECカレント")
        ECcurrent_price,ECcurrent_stock = library.ECcurrent(Amazon_partNumber)
        print("ヤマダ")
        Yamada_price,Yamada_stock = library.Yamada(Amazon_partNumber)
        print("ひかりTV")
        HikariTV_price,HikariTV_stock = library.HikariTV(Amazon_partNumber)
        print("コジマ")
        Kojima_price,Kojima_stock = library.Kojima(Amazon_partNumber)
        print("Edion")
        Edion_price,Edion_stock = library.Edion(Amazon_partNumber)
        print("Sofmap")
        Sofmap_price,Sofmap_stock = library.Sofmap(Amazon_partNumber)
        print("オムニ7")
        Omni7_price,Omni7_stock = library.Omni7(Amazon_partNumber)

        """
        #Amazonと楽天の価格差計算
        diff_rakuten = diff_price(Amazon_NEW_price,Rakuten_price,FBA_fee)
        #Amazonとヤフショの価格差計算
        diff_yahoo = diff_price(Amazon_NEW_price,Yahoo_price,FBA_fee)
        #Amazonとヨドバシの価格差計算
        diff_yodobashi = diff_price(Amazon_NEW_price,Yodobashi_price,FBA_fee)
        #Amazonとビックカメラの価格差計算
        diff_biccamera = diff_price(Amazon_NEW_price,Biccamera_price,FBA_fee)
        #Amazonとヤマダ電機の価格差計算
        diff_yamada = diff_price(Amazon_NEW_price,Yamada_price,FBA_fee)
        #AmazonとECカレントの価格差計算
        diff_eccurrent = diff_price(Amazon_NEW_price,ECcurrent_price,FBA_fee)
        #AmazonとひかりTVの価格差計算
        diff_hikaritv = diff_price(Amazon_NEW_price,HikariTV_price,FBA_fee)
        #Amazonとコジマの価格差計算
        diff_kojima = diff_price(Amazon_NEW_price,Kojima_price,FBA_fee)
        #AmazonとEdionの価格差計算
        diff_edion = diff_price(Amazon_NEW_price,Edion_price,FBA_fee)
        #AmazonとSofmapの価格差計算
        diff_sofmap = diff_price(Amazon_NEW_price,Sofmap_price,FBA_fee)
        #Amazonとオムニ7の価格差計算
        diff_omni7 = diff_price(Amazon_NEW_price,Omni7_price,FBA_fee)
        """

        message="\n{0}\nAmazon_NEW_price:{1} Amazon_BUYBOX_price:{2} Amazon_Last3mean_price:{25} \nRakuten_price:{3} Rakuten_shop:{4}\nYahoo_price:{5} Yahoo_shop:{6}\nYodobashi_price:{7} Yodobashi_stock:{8}\nBiccamera_price:{9} Biccamera_stock:{10}\nYamada_price:{11} Yamada_stock:{12}\nECcurrent_price:{13} ECcurrent_stock:{14}\nHikariTV_price:{15} HikariTV_stock:{16}\nKojima_price:{17} Kojima_stock:{18}\nEdion_price:{19} Edion_stock:{20}\nSofmap_price:{21} Sofmap_stock:{22}\nOmni7_price:{23} Omni7_stock:{24}".format(Amazon_title,Amazon_NEW_price,Amazon_Buybox_price,Rakuten_price,Rakuten_shop,Yahoo_price,Yahoo_shop,Yodobashi_price,Yodobashi_stock,Biccamera_price,Biccamera_stock,Yamada_price,Yamada_stock,ECcurrent_price,ECcurrent_stock,HikariTV_price,HikariTV_stock,Kojima_price,Kojima_stock,Edion_price,Edion_stock,Sofmap_price,Sofmap_stock,Omni7_price,Omni7_stock,Amazon_Last3mean_price)

        #過去３回分の平均を販売価格、現在の価格を仕入れ価格として粗利を計算
        diff_price = library.diff_price(Amazon_Last3mean_price,Amazon_NEW_price,FBA_fee)
        
        if(library.Purchase_decision(Amazon_Last3mean_price,diff_price) == 1):
            print("購入")
            library.send_line_notify(message)
            """
            cmd = 'C:\work\ShopDingDong_346\ShopDingDong.exe'
            url = "sample"
            quant = "quant"
            choice = "choice"
            test = "Test"
            returncode = subprocess.call(cmd, shell = True)
            """
        else:
            print("購入せず")

        print(message)
    t2 = time.time()

    print("実行時間:{0}".format(t2-t1))    

job()

#スケジュール処理
schedule.every(2).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)