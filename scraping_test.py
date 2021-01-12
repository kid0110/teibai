import requests
import time
from bs4 import BeautifulSoup

def scraping_yodobashi(url):

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    soup = BeautifulSoup(requests.get(url,headers=headers).content,"html.parser")

    line = "商品価格:{0}".format(soup.find(id='js_scl_unitPrice').text)
    print(line)

def scraping_biccamera(url):

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    soup = BeautifulSoup(requests.get(url,headers=headers).content,"html.parser")

    line = "ビック:{0}".format(soup.find(id='js_scl_unitPrice').text)
    print(line)

def scraping_saiyasune(url,num):

    headers = {
    #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66"
    }

    soup = BeautifulSoup(requests.get(url, headers=headers).content,"html.parser")


    print("-------------------------------------")
    print("#{0}:{1}".format(num,soup.find(id='p_dt12').text))

    mall_list = [tag.text for tag in soup.find_all(class_='p_dt104')]
    a_list = soup.find_all(class_='p_dt117',limit=5)
    maped_alist = map(str,a_list)
    mojiretu = ','.join(maped_alist)

    soup2 = BeautifulSoup(mojiretu,"html.parser")

    price_list=[tag.text for tag in soup2.find_all(class_=['p_dt118','p_dt119'])]
    
    result_list = zip(mall_list,price_list)


    path = 'result.txt'
    
    #price_list=soup2.find_all(class_=['p_dt118','p_dt119'])
    for result in result_list:
        print(result)

    
    with open(path,mode='w') as f:
        f.writelines(result_list)
        f.close()
    
    time.sleep(10)


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
