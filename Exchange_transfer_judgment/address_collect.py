import requests
import json

url = 'https://api.bittrex.com/api/v1.1/public/getcurrencies'
result = json.loads(requests.get(url).text)['result']
print(result)


with open('address.txt','w') as j:
    for i in result:
        j.write(str(i['Currency'])+':'+str(i['BaseAddress'])+'\n')

