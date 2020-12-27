import requests

r = requests.get('https://www.google.co.jp/')
print(r.headers['Content-Type'])
response=r
print(response.status_code)
print(response.text)   