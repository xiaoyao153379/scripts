import time
import requests
import json

def Slippage_judge(url1,url2):
    flag = True
    while flag:
        try:
            result_oder = json.loads(requests.get(url1).text)['result']
            result_history = json.loads(requests.get(url2).text)['result']
            buy = result_oder['buy']
            sell = result_oder['sell']
            buy_price = float(buy[0]['Rate'])
            sell_price = float(sell[0]['Rate'])
            flag_bslp = True
            flag_ssip = True
            for i in result_history:
                if( i['OrderType'] == 'SELL') and (flag_ssip == True):
                    sell_ID = i['Id']
                    sell_slippage = sell_price - i['Price']
                    sell_time = i['TimeStamp']
                    price_s = i['Price']
                    flag_ssip = False
                if(i['OrderType'] == 'BUY') and (flag_bslp == True):
                    buy_slippage = i['Price'] - buy_price
                    buy_time = i['TimeStamp']
                    buy_ID = i['Id']
                    price_b = i['Price']
                    flag_bslp = False
                if(flag_bslp==False) and (flag_ssip==False):
                    break
            return_data = {'sell': {'sell_ID': sell_ID, 'sell_slippage': sell_slippage, 'sell_time': sell_time,'price_s':price_s},
            'buy': {'buy_ID': buy_ID, 'buy_slippage': buy_slippage, 'buy_time': buy_time,'price_b':price_b}}
            print(return_data)
            flag = False
            return return_data
        except:
            flag = True
            time.sleep(2)
            print('erro')


url1 = 'https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-BTC&type=both'
url2 = 'https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=USD-BTC'
clock_s = 0
clock_b = 0
li_s = []
li_b = []
while True:
    result = Slippage_judge(url1,url2)
    li_s.append(result['sell'])
    clock_s += 1
    li_b.append(result['buy'])
    clock_b += 1
    if(clock_s==3000):
        with open('sell_Slippage.txt','a') as s:
            s.write(json.dumps(li_s)+'\n')
            li_s = []
            clock_s = 0
    if(clock_b==3000):
        with open('buy_Slippage.txt','a') as b:
            b.write(json.dumps(li_b)+'\n')
            li_b = []
            clock_b = 0
    time.sleep(3)