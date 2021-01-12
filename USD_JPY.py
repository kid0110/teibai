from bs4 import BeautifulSoup
import urllib.request as req
import requests
""" 
url="https://stocks.finance.yahoo.co.jp/stocks/detail/?code=usdjpy"
res = req.urlopen(url)
 
soup = BeautifulSoup(res, 'html.parser')
d1 = soup.select_one(".stoksPrice").string #(1)
print(d1)
"""
#現在の為替を取得する
def USD_JPY():
    url="https://stocks.finance.yahoo.co.jp/stocks/detail/?code=usdjpy"
    
    try:
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        d1 = soup.select_one(".stoksPrice").string
        return d1
    except:
        return 100

print(USD_JPY())