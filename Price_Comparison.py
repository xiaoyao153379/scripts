import requests
import time
import json
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from idna import unicode

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr if isinstance(addr, unicode) else addr))

def send_email(from_addr,password,to_addr,message):
    smtp_server = 'smtp.163.com'
    msg = MIMEText(message,'plain', 'utf-8')
    msg['From'] = _format_addr(u'News<%s>' % from_addr)
    msg['To'] = _format_addr(u'News <%s>' % to_addr)
    msg['Subject'] = Header(u'News', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def Get_Price1(url1):
    result = json.loads(requests.get(url1).text)
    price = result["result"][0]["Last"]
    print('bittrex: '+ str(price))
    return price

def Get_Price2(url2):
    result = json.loads(requests.get(url2).text)
    price = result['last_price']
    print('bitfinex: '+ str(price))
    return price

from_addr = ''  #the sending email account
password = '' #password
to_addr = ''#the email addr of recving
url1 = 'https://api.bittrex.com/api/v1.1/public/getmarketsummary?market=usdt-btc'#usdt-ltc/usdt-eth/usdt-xrp
url2 = "https://api.bitfinex.com/v1/pubticker/btcusd"
percent_numcer = 0.1#set limit percentage
while True:
    try:
        price_bittrex = Get_Price1(url1)
        price_bitfinex = float(Get_Price2(url2))
        if((price_bitfinex-price_bittrex)/price_bitfinex)>percent_numcer:
            message = 'bitfinex:' + str(price_bitfinex)+ '\n' + 'bittrex:' + str(price_bittrex)
            send_email(from_addr,password,to_addr,message)
    except:
        print('erro')
    time.sleep(1)
