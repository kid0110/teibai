import keepa
import pandas as pd
import matplotlib

accesskey= '1kjpjviqg2q30r3u32o4lnc96bacjj62p2hcpoj1qgnk70j7gqqe1poffs6cnncr'

asins = [
    'B0843N2NLL',
    ]

api=keepa.Keepa(accesskey)

#product_parms = {'fbaFees_gte': 3000}

#products = api.product_finder(product_parms, domain='JP')
#for product in products:
#    print(product)



products = api.query(asins,domain='JP')

for product in products:
    print(product)

data_sales = products[0]['data']['df_SALES']
data_sales.to_csv('data_sales.csv')

data_sales = products[0]['data']['df_NEW']
data_sales.to_csv('data_new.csv')