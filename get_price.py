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

def Get_Price(url):
    result = json.loads(requests.get(url).text)
    price = result["result"][0]["Last"]
    return price



from_addr = ''  #the sending email account
password = '' #password
to_addr = ''#the email addr of recving
url = 'https://api.bittrex.com/api/v1.1/public/getmarketsummary?market=usdt-btc'#usdt-ltc/usdt-eth/usdt-xrp
set_price = 4000 #set limit price
while True:
    try:
        price = Get_Price(url)
        if(price>set_price):
            send_email(from_addr, password, to_addr, str(price))
        '''
        if(price<set_price):
            send_email(from_addr, password, to_addr, str(price))
        '''
        print(price)
    except:
        print('erro')
    time.sleep(1)
