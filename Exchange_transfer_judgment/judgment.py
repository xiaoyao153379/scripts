import requests
import time
import json
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import pytz
import datetime
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

def local_to_utc(utc_format='%Y-%m-%dT%H:%M:%SZ'):
    local_tz = pytz.timezone('Asia/Chongqing')
    local_format = "%Y-%m-%d %H:%M:%S"
    time_str = time.strftime(local_format, time.localtime(time.time()))
    dt = datetime.datetime.strptime(time_str, local_format)
    local_dt = local_tz.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt.strftime(utc_format)

def judgement(url):
    flag = True
    while flag:
        try:
            result = json.loads(requests.get(url).text)['balances'][0]['value']
            flag = False
            return result
        except:
            flag = True
            time.sleep(1)

utc_time = local_to_utc()
url = 'https://data.ripple.com/v2/accounts/rPVMhWBsfF9iMXYj3aAzJVkPDTFNSyWdKy/balances?' + 'currency=XRP&date='+ utc_time +'&limit=3'
balance_fixed = float(judgement(url))
time.sleep(1)
url2 = 'https://data.ripple.com/v2/accounts/rLW9gnQo7BQhU6igk5keqYnH3TVrCxGRzm/balances?' + 'currency=XRP&date='+ utc_time +'&limit=3'
balance_fixed += float(judgement(url2))
balance_last = balance_fixed
Contrast_value = 0#Set a threshold
Contrast_value_fix = 0#Set a threshold
time.sleep(1)
from_addr = ''  #the sending email account
password = '' #password
to_addr = ''#the email addr of recving


while True:
    utc_time = local_to_utc()
    url = 'https://data.ripple.com/v2/accounts/rPVMhWBsfF9iMXYj3aAzJVkPDTFNSyWdKy/balances?'+'currency=XRP&date='+ utc_time +'&limit=3'
    balance = float(judgement(url))
    time.sleep(1)
    url2 = 'https://data.ripple.com/v2/accounts/rLW9gnQo7BQhU6igk5keqYnH3TVrCxGRzm/balances?' + 'currency=XRP&date=' + utc_time + '&limit=3'
    balance += float(judgement(url2))
    if((balance-balance_last)>Contrast_value):
        send_email(from_addr,password,to_addr,'xrp_balance:'+str(balance-balance_last))
    if((balance-balance_fixed)>Contrast_value_fix):
        send_email(from_addr,password,to_addr,'xrp_balance:'+str(balance-balance_fixed))
    time.sleep(1)
    balance_last = balance
    print(balance)


