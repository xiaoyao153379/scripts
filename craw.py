import requests
import time
import re
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


def craw_site(url,news_list):
    send_email_message = ''
    send_email_number = 0
    flag = True
    while flag:
        try:
            result = requests.get(url).text
            result = re.search('>In the.+?<div class="hl_tail ">', result, re.S)
            if (result is not None):
                result = re.findall('<div class="hl__inner">.+?</div>', result.group(), re.S)
                if (len(result) > 0):
                    for i in result:
                        news_url = re.search('href=".+?"', i, re.S)  # search the news url
                        news_title = re.search('"nofollow">.+?<', i, re.S)
                        news = news_title.group().lstrip('"nofollow"').lstrip('>').rstrip('<') + '\n' + news_url.group().lstrip(
                            'href=') + '\n---------------------'
                        if (news in news_list):
                            pass
                        else:
                            send_email_message = send_email_message + news + '\n'
                            send_email_number += 1
                            news_list.append(news)
                            print(news)
            flag = False
            return {'new_list':news_list,'send_email_message':send_email_message,'send_email_number':send_email_number}
        except:
            flag = True
            time.sleep(1)

news_list = []
url = 'https://www.newsnow.co.uk/h/Business+&+Finance/Cryptocurrencies'
from_addr = ''  #the sending email account
password = '' #password
to_addr = ''#the email addr of recving
send_email_message = ''
send_email_number = 0


while True:
    result = craw_site(url, news_list)
    send_email_number += result['send_email_number']
    news_list = result['new_list']
    if(send_email_number>0):
        send_email_message += result['send_email_message']
        send_email(from_addr, password, to_addr, '['+str(send_email_number)+']'+send_email_message)
    if(len(news_list)>200):
        for i in range(50):
            news_list.pop(index=i)
    send_email_message = ''
    send_email_number = 0
    time.sleep(1)



