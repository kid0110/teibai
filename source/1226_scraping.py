import requests
import time
import datetime
from bs4 import BeautifulSoup

def scraping_saiyasune(url,num):

    dt_now = datetime.datetime.now()
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66"
    }
    
    """
    proxy = {
        'http':'socks5://127.0.0.1:9050',
        'https':'socks5://127.0.0.1:9050'
    }"""

    try:
        soup = BeautifulSoup(requests.get(url, headers=headers).content,"html.parser")

        jancode = soup.find(id='p_dt12').text

        print("-------------------------------------")
        print("#{0}:{1}".format(num,jancode))

        a_list = soup.find_all(class_=['p_dt32','p_dt36'])
        maped_alist = map(str,a_list)
        p_dt32_list = ','.join(maped_alist)

        soup_p_dt32 = BeautifulSoup(p_dt32_list,"html.parser")
        price_list=[tag.text for tag in soup_p_dt32.find_all('td')]
        price_list.insert(0,jancode)
        price_list.insert(0,dt_now)

        maped_price_list = map(str,price_list)
        result_list = ','.join(maped_price_list)
        
        f = open('result.csv','a',encoding='UTF-8')
        f.write(result_list)
        f.write('\n')

    except AttributeError:
        print("AttributeError")

    time.sleep(20)


#-------------メイン処理-------------------

url_saiyasune= []
num = 1

f = open('jan_list.txt','r')

datalist = f.read().splitlines()

for data in datalist:
    u = "https://www.saiyasune.com/J{0}.html".format(data)
    url_saiyasune.append(u)

#print(url_saiyasune)

#url_yodobashi=["https://www.yodobashi.com/product/100000001003126076/",
#    "https://www.yodobashi.com/product/100000001005079800/",
#    "https://www.yodobashi.com/product/100000001003635708/"]

#url_saiyasune=["https://www.saiyasune.com/dt.php?sjs=1&jancode=4933621103811&js_cb1=1&js_cb1_p=3&js_cb2=1&js_cb2_p=1&js_cb3=1&js_cb5=1&js_cb6=1&js_cb7=1&js_cb8=1&js_cb11=1&js_cb12=1&js_cb13=1&js_cb15=1&js_cb16=1&js_cb17=1&js_cb18=1&js_cb19=1&js_cb20=1&js_cb21=1&js_cb23=1&js_cb24=5&js_cb34=1&js_cb50=1&js_b=1"]
#url_saiyasune=["https://www.saiyasune.com/J4932781052168.html"]
#url_saiyasune=["https://www.cman.jp/network/support/go_access.cg"]
#print("ヨドバシ")
#for u in url_yodobashi:
#    scraping_yodobashi(u)

print("最安値.com") 
for u in url_saiyasune:
    scraping_saiyasune(u,num)
    num += 1
