# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 09:29:29 2018

@author: HP
"""
import urllib, chardet, time
from bs4 import BeautifulSoup

import smtplib  
from email.mime.text import MIMEText  

log_interval = 20
interval = 30
url = "http://yz.cuc.edu.cn/class/class_2_1.html"

mailto_list = []
mail_host =        
mail_user =                    
mail_pass =                     
mail_postfix =      
              
def send_mail(to_list,sub,content):  
    me="Your Name"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)                
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)                         
        server.login(mail_user,mail_pass)              
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception as e:  
        print(e)  
        return False  
                       

def get_content(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    charset = chardet.detect(html)
    html = html.decode(charset['encoding'])
    soup = BeautifulSoup(html, 'lxml')
    response.close() 
    return soup

def compare_time(later_time, former_time):
    return int(later_time.replace('-', '')[1:-1]) - int(former_time.replace('-', '')[1:-1])

def get_news(soup):
    news_times = soup.select('body > #content > #left > .left_news > .class > p > span')
    origin_time = time.strftime("[%Y-%m-%d]")
    times = []
    for i in range(len(news_times)):
        latest_time = news_times[i].get_text()
        if compare_time(latest_time, origin_time) >= 0:
            times.append(latest_time)
            
    all_news = soup.select('body > #content > #left > .left_news > .class > p > a')
    news = []
    for i in range(len(times)):
        news.append(all_news[i].get_text())
    
    links = ['http://yz.cuc.edu.cn' + link.get('href')[2:] for link in soup.find_all('a')]
    links = links[1: len(times) + 1]
        
    message = ''
    for i, j, k in zip(times, news, links):
        message += i + j + '\n'+ k  + '\n\n'

    return message 

if __name__ == '__main__':
    start = time.time()
    print("Monitor is running:")
    print("=" * 75)
    
    old_message = []
    count = 0
    while(True):
        soup = get_content(url)
        message = get_news(soup)        
        
        if message != '' and old_message != message:
            old_message = message
            print(message)
            send_mail(mailto_list,"中国传媒大学研招网有更新", str(message))
        else:
            if count % log_interval == 0:
                print("No New News")
        if count % log_interval == 0:
            print("Monitor has been running for : %d minutes" % int((time.time() - start)/60))
            print("-"*75)
        time.sleep(interval)
        count += 1
    