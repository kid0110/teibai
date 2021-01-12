import requests

url = 'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch'

params = {
    'appid': 'dj00aiZpPUNuaW5OSjZtclp5MiZzPWNvbnN1bWVyc2VjcmV0Jng9ZDk-', 
    'jan_code': '4933621104832',
    'sort': '+price'
}

r = requests.get(url,params=params)
resp = r.json()

print(resp['hits'][0]['price'])
print(resp['hits'][0]['seller']['name'])

"""
url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706'

params = {
    'applicationId': '1083938945783823235',
    'keyword': '4933621104832',
    'sort': '+itemPrice'
}

r = requests.get(url,params=params)
resp = r.json()

print(resp['Items'][0]['Item']['itemPrice'])

counter = 0
for i in resp['Items']:
    counter = counter + 1
    item = i['Item']
    name = item['itemName']
    print( '【No.】'+ str(counter))
    print('【Name】' + str(name[:30].encode('utf-8')) + '...') 
    print('【Price】' + '¥' +str(item['itemPrice']))
    print('【URL】',item['itemUrl'])
    print('【shop】',item['shopName'])
    print('【text】', item['itemCaption'])
"""